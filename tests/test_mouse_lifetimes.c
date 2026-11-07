/* SPDX-License-Identifier: MIT */
#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>

#define LOG_INF(...) ((void)0)
#define LOG_ERR(...) ((void)0)
#define LOG_DBG(...) ((void)0)
#define ZMK_EV_EVENT_BUBBLE 0
#define ZMK_BEHAVIOR_OPAQUE 0
#define ZMK_KEYMAP_LAYERS_LEN 8
#define K_NO_WAIT 0
#define K_MSEC(ms) (ms)
#define CONTAINER_OF(p, t, m) ((t *)((char *)(p)-offsetof(t,m)))
#define ZMK_HID_USAGE_PAGE(k) ((k) >> 16)
#define ZMK_HID_USAGE_ID(k) ((k) & 65535)
#define HID_USAGE_KEY 7
typedef uint8_t zmk_keymap_layer_id_t;
#define ZMK_KEYMAP_LAYER_ID_INVAL UINT8_MAX
struct k_work { int unused; };
struct k_work_delayable { struct k_work work; bool pending; int64_t deadline; };
static int64_t now;
static int64_t k_uptime_get(void) { return now; }
static struct k_work_delayable *k_work_delayable_from_work(struct k_work *w) { return (void *)w; }
static int k_work_reschedule(struct k_work_delayable *w, int64_t ms) {
    w->pending=true; w->deadline=now+ms; return 0;
}
static int k_work_cancel_delayable(struct k_work_delayable *w) { w->pending=false; return 0; }
struct device { const void *config; void *data; };
struct runtime_processor_data {
    const struct device *dev;
    bool temp_layer_enabled, temp_layer_layer_active, temp_layer_keep_active;
    uint8_t temp_layer_layer;
    uint16_t temp_layer_activation_delay_ms, temp_layer_deactivation_delay_ms;
    uint64_t temp_layer_held_positions;
    int64_t last_input_timestamp, last_keypress_timestamp;
    struct k_work_delayable temp_layer_activation_work, temp_layer_deactivation_work;
    bool inertia_active;
    uint32_t active_layers;
};
struct runtime_processor_config {
    const struct device *temp_layer_transparent_behavior, *temp_layer_kp_behavior;
    size_t temp_layer_keep_keycodes_len;
    const uint16_t *temp_layer_keep_keycodes;
};
struct zmk_behavior_binding { const char *behavior_dev; uint32_t param1, param2; };
struct zmk_behavior_binding_event { int layer; uint32_t position; int64_t timestamp; };
struct zmk_position_state_changed { uint32_t position; bool state; };
struct zmk_layer_state_changed { uint8_t layer; bool state; };
typedef struct { bool layer_event; uint32_t position; bool state; uint8_t layer; } zmk_event_t;
static const struct zmk_position_state_changed *as_zmk_position_state_changed(const zmk_event_t *e) {
    static struct zmk_position_state_changed v; v.position=e->position; v.state=e->state;
    return e->layer_event ? NULL : &v;
}
static const struct zmk_layer_state_changed *as_zmk_layer_state_changed(const zmk_event_t *e) {
    static struct zmk_layer_state_changed v; v.layer=e->layer; v.state=e->state;
    return e->layer_event ? &v : NULL;
}
static bool layer_active[8];
static struct device trans_dev, kp_dev, click_dev;
static struct runtime_processor_data data0;
static struct runtime_processor_config cfg;
static struct device mouse_dev={.config=&cfg,.data=&data0};
static const struct device *runtime_processors[]={&mouse_dev};
static size_t runtime_processors_count=1;
static struct zmk_behavior_binding bindings[8][47];
static bool zmk_keymap_layer_active(uint8_t layer) { return layer_active[layer]; }
static int zmk_keymap_layer_activate(uint8_t layer, bool locking) { layer_active[layer]=true; return 0; }
static int zmk_keymap_layer_deactivate(uint8_t layer, bool locking) { layer_active[layer]=false; return 0; }
static uint8_t zmk_keymap_layer_index_to_id(uint8_t index) { return index; }
static const struct zmk_behavior_binding *zmk_keymap_get_layer_binding_at_idx(uint8_t layer, uint32_t pos) {
    return pos < 47 ? &bindings[layer][pos] : NULL;
}
struct wheel_config { uint16_t code; int32_t step; };
static struct wheel_config wheel_cfg={8,-1};
static struct device wheel_dev={.config=&wheel_cfg};
static const struct device *zmk_behavior_get_binding(const char *name) {
    if (!strcmp(name,"trans")) return &trans_dev;
    if (!strcmp(name,"kp")) return &kp_dev;
    if (!strcmp(name,"wheel")) return &wheel_dev;
    return &click_dev;
}
static bool is_mod(uint16_t page, uint16_t usage) { return page==7 && usage>=224 && usage<=231; }
static bool is_processor_active_for_current_layers(uint32_t mask) { return true; }
#define ZMK_INPUT_PROCESSOR_INERTIA_STOP_REASON_LAYER_INACTIVE 1
static void inertia_stop(struct runtime_processor_data *d, int reason) { d->inertia_active=false; }
struct input_event { int32_t value; };
static const struct device *zmk_input_processor_runtime_find_by_name(const char *name) { return &mouse_dev; }
static int reports, wheel_total;
static int input_report_rel(const struct device *dev, uint16_t code, int32_t value, bool sync, int timeout) {
    assert(dev==&wheel_dev && sync && timeout==K_NO_WAIT);
    assert(code==wheel_cfg.code && (value==1 || value==-1));
    reports++; wheel_total+=value; return 0;
}

#include "runtime_functions.inc"

static void reset(void) {
    memset(&data0,0,sizeof(data0)); memset(layer_active,0,sizeof(layer_active));
    data0.dev=&mouse_dev; data0.temp_layer_enabled=true; data0.temp_layer_layer=1;
    data0.temp_layer_activation_delay_ms=200; data0.temp_layer_deactivation_delay_ms=1200;
    layer_active[0]=true; now=1000; cfg.temp_layer_transparent_behavior=&trans_dev;
    cfg.temp_layer_kp_behavior=&kp_dev;
    for (int l=0;l<8;l++) for (int p=0;p<47;p++) {
        bindings[l][p]=(struct zmk_behavior_binding){l ? "trans" : "kp",4,0};
    }
    bindings[1][19].behavior_dev="click"; bindings[1][20].behavior_dev="click";
    bindings[0][36].param1=224;
}
static void move(void) { struct input_event e={1}; motion(&e); }
static void activate(void) {
    assert(data0.temp_layer_activation_work.pending);
    data0.temp_layer_activation_work.pending=false;
    temp_layer_activation_work_handler(&data0.temp_layer_activation_work.work);
}
static void expire(void) {
    data0.temp_layer_deactivation_work.pending=false;
    temp_layer_deactivation_work_handler(&data0.temp_layer_deactivation_work.work);
}
static void key(uint32_t pos, bool down) {
    zmk_event_t e={.position=pos,.state=down}; position_state_changed_listener(&e);
}
int main(void) {
    reset(); move(); activate(); assert(layer_active[1]);
    assert(data0.temp_layer_deactivation_work.deadline==2200); /* one frame expires */
    now=2200; expire(); assert(!layer_active[1]);
    reset(); key(10,true); now=1199; move(); assert(!data0.temp_layer_activation_work.pending);
    now=1200; move(); activate(); assert(layer_active[1]); /* typing guard */
    reset(); move(); activate(); now=2100; zmk_input_processor_runtime_note_activity(&mouse_dev);
    now=2200; expire(); assert(layer_active[1] && data0.temp_layer_deactivation_work.deadline==3300);
    now=3300; expire(); assert(!layer_active[1]); /* stale expiry cannot win */
    reset(); move(); activate(); now=2000; key(19,true); now=2200; expire(); assert(layer_active[1]);
    now=2300; key(20,true); now=3000; key(19,false); now=6000; expire(); assert(layer_active[1]);
    key(20,false); assert(data0.temp_layer_deactivation_work.deadline==7200);
    now=7200; expire(); assert(!layer_active[1]); /* two buttons / long drag */
    reset(); move(); activate(); key(36,true); now=5000; expire(); assert(layer_active[1]);
    key(36,false); assert(data0.temp_layer_deactivation_work.deadline==6200); /* modifier drag */
    reset(); move(); activate(); key(10,true); assert(!layer_active[1]); /* normal typing exits */
    reset(); layer_active[1]=true; move(); activate(); assert(!data0.temp_layer_layer_active);
    assert(!data0.temp_layer_deactivation_work.pending); /* manual layer is not owned */
    reset(); move(); activate();
    zmk_event_t off={.layer_event=true,.layer=1,.state=false}; layer_active[1]=false;
    runtime_processor_layer_state_changed_listener(&off); assert(!data0.temp_layer_layer_active);
    move(); activate(); assert(layer_active[1]); /* explicit exit can re-enter */
    struct zmk_behavior_binding binding={"wheel",0,0}; struct zmk_behavior_binding_event event={0};
    reports=wheel_total=0; now=2100; assert(!pressed(&binding,event)); assert(reports==1 && wheel_total==-1);
    assert(!released(&binding,event) && reports==1);
    assert(data0.temp_layer_deactivation_work.deadline==3300); /* encoder extends active layer */
    for (int i=0;i<1000;i++) { pressed(&binding,event); released(&binding,event); }
    assert(reports==1001 && wheel_total==-1001);
    wheel_cfg.step=1; pressed(&binding,event); assert(wheel_total==-1000);
    puts("Mouse lifetime and discrete wheel regression tests passed");
    return 0;
}
