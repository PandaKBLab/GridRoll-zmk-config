/* SPDX-License-Identifier: MIT */
#include <assert.h>
#include <stdio.h>
#include "status_policy.h"

static struct gr_status s;
static void init(bool right) {
    gr_status_init(&s,right);
    gr_status_activity(&s,true,0);
}
int main(void) {
    init(false);
    assert(!gr_status_render(&s,0).on); /* startup zero is not a sample */
    gr_status_sample(&s,0,0,100);
    assert(gr_status_render(&s,100).on); /* real 0% must warn */
    assert(!gr_status_render(&s,200).on);
    assert(gr_status_render(&s,30100).on);
    gr_status_sample(&s,0,17,30200); assert(s.low); /* hysteresis */
    gr_status_sample(&s,0,20,30300); assert(!s.low);
    assert(gr_status_render(&s,30300).next==-1);
    gr_status_sample(&s,0,15,31000); assert(gr_status_render(&s,31000).on);
    s.usb=true; assert(!gr_status_render(&s,31001).on); /* charge suppresses low */
    assert(gr_status_render(&s,31001).next==-1);
    s.usb=false; gr_status_sample(&s,-1,15,32000);
    assert(!gr_status_render(&s,32000).on); /* failed fetch is not fresh cached SOC */
    gr_status_sample(&s,0,10,33000);
    assert(!gr_status_render(&s,213000).on); /* no samples for 180 s */
    assert(gr_status_render(&s,213000).next==-1);
    gr_status_sample(&s,0,100,214000);
    assert(!gr_status_render(&s,214000).on); /* no software 'full' lamp */
    init(true); gr_status_link(&s,true,false,0,1000);
    int on_edges=0;
    for (int64_t t=1000;t<31000;t+=100) {
        gr_status_link(&s,true,false,0,t); /* repeated callbacks do not renew */
        struct gr_render r=gr_status_render(&s,t);
        if(r.on) on_edges++;
    }
    assert(on_edges==15);
    assert(gr_status_render(&s,31000).next==-1);
    gr_status_sample(&s,0,80,32000);
    assert(gr_status_render(&s,32000).next==-1); /* battery sample cannot restart waiting */
    gr_status_link(&s,true,true,0,33000);
    assert(gr_status_render(&s,33000).on);
    gr_status_link(&s,true,true,0,34000);
    assert(gr_status_render(&s,34999).on);
    assert(gr_status_render(&s,35000).next==-1); /* connected=off, no periodic work */
    gr_status_link(&s,true,false,0,36000); assert(gr_status_render(&s,36000).on);
    gr_status_link(&s,false,false,0,36001);
    assert(gr_status_render(&s,36001).next==-1); /* normal wired output */
    gr_status_link(&s,true,false,1,37000); assert(gr_status_render(&s,37000).on);
    gr_status_sample(&s,0,10,37100);
    assert(gr_status_render(&s,37100).on);
    assert(!gr_status_render(&s,39000).on); /* low battery suppresses waiting flash */
    gr_status_link(&s,true,true,1,40000); assert(gr_status_render(&s,40000).on);
    assert(gr_status_render(&s,41999).on); /* connection confirmation still visible */
    assert(!gr_status_render(&s,42000).on); /* back to low-battery timing */
    gr_status_activity(&s,false,42001);
    assert(gr_status_render(&s,42001).next==-1 && !s.valid);
    gr_status_sample(&s,0,0,43000);
    assert(gr_status_render(&s,43000).next==-1 && !s.valid); /* late sample while idle */
    gr_status_activity(&s,true,44000);
    assert(!s.valid); /* wake needs a new fetch */
    gr_status_sample(&s,0,25,44001); assert(!s.low);
    gr_status_activity(&s,false,44002);
    assert(gr_status_render(&s,1000000).next==-1);
    init(false); gr_status_link(&s,true,true,0,1);
    assert(gr_status_render(&s,1).next==-1); /* left never reports host connection */
    gr_status_link(&s,true,false,1,2);
    assert(gr_status_render(&s,2).next==-1);
    puts("LED policy: bounded waiting, connection, hysteresis, USB, stale/failed/zero samples, left role and idle/wake passed");
    return 0;
}
