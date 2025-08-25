                Introduction to clustered tables  |  BigQuery  |  Google Cloud    { "@context": "https://schema.org", "@type": "Article", "headline": "Introduction to clustered tables" } { "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": \[{ "@type": "ListItem", "position": 1, "name": "BigQuery", "item": "https://cloud.google.com/bigquery" },{ "@type": "ListItem", "position": 2, "name": "Documentation", "item": "https://cloud.google.com/bigquery/docs" },{ "@type": "ListItem", "position": 3, "name": "Introduction to clustered tables", "item": "https://cloud.google.com/bigquery/docs/clustered-tables" }\] }    .gb\_4d{font:13px/27px Roboto,Arial,sans-serif;z-index:986}@-webkit-keyframes gb\_\_a{0%{opacity:0}50%{opacity:1}}@keyframes gb\_\_a{0%{opacity:0}50%{opacity:1}}a.gb\_Qa{border:none;color:#4285f4;cursor:default;font-weight:bold;outline:none;position:relative;text-align:center;text-decoration:none;text-transform:uppercase;white-space:nowrap;-webkit-user-select:none}a.gb\_Qa:hover::after,a.gb\_Qa:focus::after{background-color:rgba(0,0,0,.12);content:"";height:100%;left:0;position:absolute;top:0;width:100%}a.gb\_Qa:hover,a.gb\_Qa:focus{text-decoration:none}a.gb\_Qa:active{background-color:rgba(153,153,153,.4);text-decoration:none}a.gb\_Ra{background-color:#4285f4;color:#fff}a.gb\_Ra:active{background-color:#0043b2}.gb\_Sa{box-shadow:0 1px 1px rgba(0,0,0,.16)}.gb\_Qa,.gb\_Ra,.gb\_Ta,.gb\_Ua{display:inline-block;line-height:28px;padding:0 12px;border-radius:2px}.gb\_Ta{background:#f8f8f8;border:1px solid #c6c6c6}.gb\_Ua{background:#f8f8f8}.gb\_Ta,#gb a.gb\_Ta.gb\_Ta,.gb\_Ua{color:#666;cursor:default;text-decoration:none}#gb a.gb\_Ua{cursor:default;text-decoration:none}.gb\_Ua{border:1px solid #4285f4;font-weight:bold;outline:none;background:#4285f4;background:-webkit-gradient(linear,left top,left bottom,from(top),color-stop(#4387fd),to(#4683ea));background:-webkit-linear-gradient(top,#4387fd,#4683ea);background:linear-gradient(top,#4387fd,#4683ea);filter:progid:DXImageTransform.Microsoft.gradient(startColorstr=#4387fd,endColorstr=#4683ea,GradientType=0)}#gb a.gb\_Ua{color:#fff}.gb\_Ua:hover{box-shadow:0 1px 0 rgba(0,0,0,.15)}.gb\_Ua:active{box-shadow:inset 0 2px 0 rgba(0,0,0,.15);background:#3c78dc;background:-webkit-gradient(linear,left top,left bottom,from(top),color-stop(#3c7ae4),to(#3f76d3));background:-webkit-linear-gradient(top,#3c7ae4,#3f76d3);background:linear-gradient(top,#3c7ae4,#3f76d3);filter:progid:DXImageTransform.Microsoft.gradient(startColorstr=#3c7ae4,endColorstr=#3f76d3,GradientType=0)}#gb .gb\_Va{background:#fff;border:1px solid #dadce0;color:#1a73e8;display:inline-block;text-decoration:none}#gb .gb\_Va:hover{background:#f8fbff;border-color:#dadce0;color:#174ea6}#gb .gb\_Va:focus{background:#f4f8ff;color:#174ea6;outline:1px solid #174ea6}#gb .gb\_Va:active,#gb .gb\_Va:focus:active{background:#ecf3fe;color:#174ea6}#gb .gb\_Va.gb\_H{background:transparent;border:1px solid #5f6368;color:#8ab4f8;text-decoration:none}#gb .gb\_Va.gb\_H:hover{background:rgba(255,255,255,.04);color:#e8eaed}#gb .gb\_Va.gb\_H:focus{background:rgba(232,234,237,.12);color:#e8eaed;outline:1px solid #e8eaed}#gb .gb\_Va.gb\_H:active,#gb .gb\_Va.gb\_H:focus:active{background:rgba(232,234,237,.1);color:#e8eaed}.gb\_dd{display:inline-block;vertical-align:middle}.gb\_Qe .gb\_Q{bottom:-3px;right:-5px}.gb\_D{position:relative}.gb\_B{display:inline-block;outline:none;vertical-align:middle;border-radius:2px;box-sizing:border-box;height:40px;width:40px;cursor:pointer;text-decoration:none}#gb#gb a.gb\_B{cursor:pointer;text-decoration:none}.gb\_B,a.gb\_B{color:#000}.gb\_ed{border-color:transparent;border-bottom-color:#fff;border-style:dashed dashed solid;border-width:0 8.5px 8.5px;display:none;position:absolute;left:11.5px;top:33px;z-index:1;height:0;width:0;-webkit-animation:gb\_\_a .2s;animation:gb\_\_a .2s}.gb\_fd{border-color:transparent;border-style:dashed dashed solid;border-width:0 8.5px 8.5px;display:none;position:absolute;left:11.5px;z-index:1;height:0;width:0;-webkit-animation:gb\_\_a .2s;animation:gb\_\_a .2s;border-bottom-color:rgba(0,0,0,.2);top:32px}x:-o-prefocus,div.gb\_fd{border-bottom-color:#ccc}.gb\_la{background:#fff;border:1px solid #ccc;border-color:rgba(0,0,0,.2);color:#000;-webkit-box-shadow:0 2px 10px rgba(0,0,0,.2);box-shadow:0 2px 10px rgba(0,0,0,.2);display:none;outline:none;overflow:hidden;position:absolute;right:8px;top:62px;-webkit-animation:gb\_\_a .2s;animation:gb\_\_a .2s;border-radius:2px;-webkit-user-select:text}.gb\_dd.gb\_Uc .gb\_ed,.gb\_dd.gb\_Uc .gb\_fd,.gb\_dd.gb\_Uc .gb\_la,.gb\_Uc.gb\_la{display:block}.gb\_dd.gb\_Uc.gb\_gd .gb\_ed,.gb\_dd.gb\_Uc.gb\_gd .gb\_fd{display:none}.gb\_Re{position:absolute;right:8px;top:62px;z-index:-1}.gb\_hd .gb\_ed,.gb\_hd .gb\_fd,.gb\_hd .gb\_la{margin-top:-10px}.gb\_dd:first-child,#gbsfw:first-child+.gb\_dd{padding-left:4px}.gb\_Fa.gb\_Se .gb\_dd:first-child{padding-left:0}.gb\_Te{position:relative}.gb\_3c .gb\_Te,.gb\_Kd .gb\_Te{float:right}.gb\_B{padding:8px;cursor:pointer}.gb\_B::after{content:"";position:absolute;top:-4px;bottom:-4px;left:-4px;right:-4px}.gb\_Fa .gb\_id:not(.gb\_Qa):focus img{background-color:rgba(0,0,0,.2);outline:none;-webkit-border-radius:50%;border-radius:50%}.gb\_jd button svg,.gb\_B{-webkit-border-radius:50%;border-radius:50%}.gb\_jd button:focus:not(:focus-visible) svg,.gb\_jd button:hover svg,.gb\_jd button:active svg,.gb\_B:focus:not(:focus-visible),.gb\_B:hover,.gb\_B:active,.gb\_B\[aria-expanded=true\]{outline:none}.gb\_Mc .gb\_jd.gb\_kd button:focus-visible svg,.gb\_jd button:focus-visible svg,.gb\_B:focus-visible{outline:1px solid #202124}.gb\_Mc .gb\_jd button:focus-visible svg,.gb\_Mc .gb\_B:focus-visible{outline:1px solid #f1f3f4}@media (forced-colors:active){.gb\_Mc .gb\_jd.gb\_kd button:focus-visible svg,.gb\_jd button:focus-visible svg,.gb\_Mc .gb\_jd button:focus-visible svg{outline:1px solid currentcolor}}.gb\_Mc .gb\_jd.gb\_kd button:focus svg,.gb\_Mc .gb\_jd.gb\_kd button:focus:hover svg,.gb\_jd button:focus svg,.gb\_jd button:focus:hover svg,.gb\_B:focus,.gb\_B:focus:hover{background-color:rgba(60,64,67,.1)}.gb\_Mc .gb\_jd.gb\_kd button:active svg,.gb\_jd button:active svg,.gb\_B:active{background-color:rgba(60,64,67,.12)}.gb\_Mc .gb\_jd.gb\_kd button:hover svg,.gb\_jd button:hover svg,.gb\_B:hover{background-color:rgba(60,64,67,.08)}.gb\_Wa .gb\_B.gb\_Za:hover{background-color:transparent}.gb\_B\[aria-expanded=true\],.gb\_B:hover\[aria-expanded=true\]{background-color:rgba(95,99,104,.24)}.gb\_B\[aria-expanded=true\] .gb\_F{fill:#5f6368;opacity:1}.gb\_Mc .gb\_jd button:hover svg,.gb\_Mc .gb\_B:hover{background-color:rgba(232,234,237,.08)}.gb\_Mc .gb\_jd button:focus svg,.gb\_Mc .gb\_jd button:focus:hover svg,.gb\_Mc .gb\_B:focus,.gb\_Mc .gb\_B:focus:hover{background-color:rgba(232,234,237,.1)}.gb\_Mc .gb\_jd button:active svg,.gb\_Mc .gb\_B:active{background-color:rgba(232,234,237,.12)}.gb\_Mc .gb\_B\[aria-expanded=true\],.gb\_Mc .gb\_B:hover\[aria-expanded=true\]{background-color:rgba(255,255,255,.12)}.gb\_Mc .gb\_B\[aria-expanded=true\] .gb\_F{fill:#fff;opacity:1}.gb\_dd{padding:4px}.gb\_Fa.gb\_Se .gb\_dd{padding:4px 2px}.gb\_Fa.gb\_Se .gb\_z.gb\_dd{padding-left:6px}.gb\_la{z-index:991;line-height:normal}.gb\_la.gb\_ld{left:0;right:auto}@media (max-width:350px){.gb\_la.gb\_ld{left:0}}.gb\_Ue .gb\_la{top:56px}.gb\_R{display:none!important}.gb\_od{visibility:hidden}.gb\_J .gb\_B,.gb\_ka .gb\_J .gb\_B{background-position:-64px -29px}.gb\_1 .gb\_J .gb\_B{background-position:-29px -29px;opacity:1}.gb\_J .gb\_B,.gb\_J .gb\_B:hover,.gb\_J .gb\_B:focus{opacity:1}.gb\_L{display:none}@media screen and (max-width:319px){.gb\_md:not(.gb\_nd) .gb\_J{display:none;visibility:hidden}}.gb\_Q{display:none}.gb\_ad{font-family:Google Sans,Roboto,Helvetica,Arial,sans-serif;font-size:20px;font-weight:400;letter-spacing:0.25px;line-height:48px;margin-bottom:2px;opacity:1;overflow:hidden;padding-left:16px;position:relative;text-overflow:ellipsis;vertical-align:middle;top:2px;white-space:nowrap;-webkit-flex:1 1 auto;-webkit-box-flex:1;flex:1 1 auto}.gb\_ad.gb\_bd{color:#3c4043}.gb\_Fa.gb\_cc .gb\_ad{margin-bottom:0}.gb\_td.gb\_vd .gb\_ad{padding-left:4px}.gb\_Fa.gb\_cc .gb\_wd{position:relative;top:-2px}.gb\_cd{display:none}.gb\_Fa{color:black;min-width:160px;position:relative;-webkit-transition:box-shadow 250ms;transition:box-shadow 250ms}.gb\_Fa.gb\_Tc{min-width:120px}.gb\_Fa.gb\_xd .gb\_yd{display:none}.gb\_Fa.gb\_xd .gb\_md{height:56px}header.gb\_Fa{display:block}.gb\_Fa svg{fill:currentColor}.gb\_Ed{position:fixed;top:0;width:100%}.gb\_zd{-webkit-box-shadow:0 4px 5px 0 rgba(0,0,0,.14),0 1px 10px 0 rgba(0,0,0,.12),0 2px 4px -1px rgba(0,0,0,.2);box-shadow:0 4px 5px 0 rgba(0,0,0,.14),0 1px 10px 0 rgba(0,0,0,.12),0 2px 4px -1px rgba(0,0,0,.2)}.gb\_Fd{height:64px}.gb\_md{-webkit-box-sizing:border-box;box-sizing:border-box;position:relative;width:100%;display:-webkit-box;display:-webkit-flex;display:flex;-webkit-box-pack:space-between;-webkit-justify-content:space-between;justify-content:space-between;min-width:-webkit-min-content;min-width:min-content}.gb\_Fa:not(.gb\_cc) .gb\_md{padding:8px}.gb\_Fa.gb\_Hd .gb\_md{-webkit-flex:1 0 auto;-webkit-box-flex:1;flex:1 0 auto}.gb\_Fa .gb\_md.gb\_nd.gb\_Id{min-width:0}.gb\_Fa.gb\_cc .gb\_md{padding:4px;padding-left:8px;min-width:0}.gb\_yd{height:48px;vertical-align:middle;white-space:nowrap;-webkit-box-align:center;-webkit-align-items:center;align-items:center;display:-webkit-box;display:-webkit-flex;display:flex;-webkit-user-select:none}.gb\_Bd>.gb\_yd{display:table-cell;width:100%}.gb\_td{padding-right:30px;box-sizing:border-box;-webkit-flex:1 0 auto;-webkit-box-flex:1;flex:1 0 auto}.gb\_Fa.gb\_cc .gb\_td{padding-right:14px}.gb\_Cd{-webkit-flex:1 1 100%;-webkit-box-flex:1;flex:1 1 100%}.gb\_Cd>:only-child{display:inline-block}.gb\_Dd.gb\_4c{padding-left:4px}.gb\_Dd.gb\_Jd,.gb\_Fa.gb\_Hd .gb\_Dd,.gb\_Fa.gb\_cc:not(.gb\_Kd) .gb\_Dd{padding-left:0}.gb\_Fa.gb\_cc .gb\_Dd.gb\_Jd{padding-right:0}.gb\_Fa.gb\_cc .gb\_Dd.gb\_Jd .gb\_Wa{margin-left:10px}.gb\_4c{display:inline}.gb\_Fa.gb\_Xc .gb\_Dd.gb\_Ld,.gb\_Fa.gb\_Kd .gb\_Dd.gb\_Ld{padding-left:2px}.gb\_ad{display:inline-block}.gb\_Dd{-webkit-box-sizing:border-box;box-sizing:border-box;height:48px;line-height:normal;padding:0 4px;padding-left:30px;-webkit-flex:0 0 auto;-webkit-box-flex:0;flex:0 0 auto;-webkit-box-pack:flex-end;-webkit-justify-content:flex-end;justify-content:flex-end}.gb\_Kd{height:48px}.gb\_Fa.gb\_Kd{min-width:auto}.gb\_Kd .gb\_Dd{float:right;padding-left:32px}.gb\_Kd .gb\_Dd.gb\_Md{padding-left:0}.gb\_Nd{font-size:14px;max-width:200px;overflow:hidden;padding:0 12px;text-overflow:ellipsis;white-space:nowrap;-webkit-user-select:text}.gb\_qd{-webkit-transition:background-color .4s;-webkit-transition:background-color .4s;transition:background-color .4s}.gb\_Od{color:black}.gb\_Mc{color:white}.gb\_Fa a,.gb\_Qc a{color:inherit}.gb\_ba{color:rgba(0,0,0,.87)}.gb\_Fa svg,.gb\_Qc svg,.gb\_td .gb\_ud,.gb\_3c .gb\_ud{color:#5f6368;opacity:1}.gb\_Mc svg,.gb\_Qc.gb\_Vc svg,.gb\_Mc .gb\_td .gb\_ud,.gb\_Mc .gb\_td .gb\_Lc,.gb\_Mc .gb\_td .gb\_wd,.gb\_Qc.gb\_Vc .gb\_ud{color:rgba(255,255,255,.87)}.gb\_Mc .gb\_td .gb\_Pd:not(.gb\_Qd){opacity:.87}.gb\_bd{color:inherit;opacity:1;text-rendering:optimizeLegibility;-webkit-font-smoothing:antialiased}.gb\_Mc .gb\_bd,.gb\_Od .gb\_bd{opacity:1}.gb\_Rd{position:relative}.gb\_M{font-family:arial,sans-serif;line-height:normal;padding-right:15px}a.gb\_X,span.gb\_X{color:rgba(0,0,0,.87);text-decoration:none}.gb\_Mc a.gb\_X,.gb\_Mc span.gb\_X{color:white}a.gb\_X:focus{outline-offset:2px}a.gb\_X:hover{text-decoration:underline}.gb\_Z{display:inline-block;padding-left:15px}.gb\_Z .gb\_X{display:inline-block;line-height:24px;vertical-align:middle}.gb\_rd{font-family:Google Sans,Roboto,Helvetica,Arial,sans-serif;font-weight:500;font-size:14px;letter-spacing:.25px;line-height:16px;margin-left:10px;margin-right:8px;min-width:96px;padding:9px 23px;text-align:center;vertical-align:middle;border-radius:4px;box-sizing:border-box}.gb\_Fa.gb\_Kd .gb\_rd{margin-left:8px}#gb a.gb\_Ua.gb\_rd{cursor:pointer}.gb\_Ua.gb\_rd:hover{background:#1b66c9;-webkit-box-shadow:0 1px 3px 1px rgba(66,64,67,.15),0 1px 2px 0 rgba(60,64,67,.3);box-shadow:0 1px 3px 1px rgba(66,64,67,.15),0 1px 2px 0 rgba(60,64,67,.3)}.gb\_Ua.gb\_rd:focus,.gb\_Ua.gb\_rd:hover:focus{background:#1c5fba;-webkit-box-shadow:0 1px 3px 1px rgba(66,64,67,.15),0 1px 2px 0 rgba(60,64,67,.3);box-shadow:0 1px 3px 1px rgba(66,64,67,.15),0 1px 2px 0 rgba(60,64,67,.3)}.gb\_Ua.gb\_rd:active{background:#1b63c1;-webkit-box-shadow:0 1px 3px 1px rgba(66,64,67,.15),0 1px 2px 0 rgba(60,64,67,.3);box-shadow:0 1px 3px 1px rgba(66,64,67,.15),0 1px 2px 0 rgba(60,64,67,.3)}.gb\_rd{background:#1a73e8;border:1px solid transparent}.gb\_Fa.gb\_cc .gb\_rd{padding:9px 15px;min-width:80px}.gb\_Sd{text-align:left}#gb .gb\_Mc a.gb\_rd:not(.gb\_H),#gb.gb\_Mc a.gb\_rd{background:#fff;border-color:#dadce0;-webkit-box-shadow:none;box-shadow:none;color:#1a73e8}#gb a.gb\_Ua.gb\_H.gb\_rd{background:#8ab4f8;border:1px solid transparent;-webkit-box-shadow:none;box-shadow:none;color:#202124}#gb .gb\_Mc a.gb\_rd:hover:not(.gb\_H),#gb.gb\_Mc a.gb\_rd:hover{background:#f8fbff;border-color:#cce0fc}#gb a.gb\_Ua.gb\_H.gb\_rd:hover{background:#93baf9;border-color:transparent;-webkit-box-shadow:0 1px 3px 1px rgba(0,0,0,.15),0 1px 2px rgba(0,0,0,.3);box-shadow:0 1px 3px 1px rgba(0,0,0,.15),0 1px 2px rgba(0,0,0,.3)}#gb .gb\_Mc a.gb\_rd:focus:not(.gb\_H),#gb .gb\_Mc a.gb\_rd:focus:hover:not(.gb\_H),#gb.gb\_Mc a.gb\_rd:focus:not(.gb\_H),#gb.gb\_Mc a.gb\_rd:focus:hover:not(.gb\_H){background:#f4f8ff;outline:1px solid #c9ddfc}#gb a.gb\_Ua.gb\_H.gb\_rd:focus,#gb a.gb\_Ua.gb\_H.gb\_rd:focus:hover{background:#a6c6fa;border-color:transparent;-webkit-box-shadow:none;box-shadow:none}#gb .gb\_Mc a.gb\_rd:active:not(.gb\_H),#gb.gb\_Mc a.gb\_rd:active{background:#ecf3fe}#gb a.gb\_Ua.gb\_H.gb\_rd:active{background:#a1c3f9;-webkit-box-shadow:0 1px 2px rgba(60,64,67,.3),0 2px 6px 2px rgba(60,64,67,.15);box-shadow:0 1px 2px rgba(60,64,67,.3),0 2px 6px 2px rgba(60,64,67,.15)}.gb\_K{display:none}@media screen and (max-width:319px){.gb\_md .gb\_J{display:none;visibility:hidden}}.gb\_Wa{background-color:rgba(255,255,255,.88);border:1px solid #dadce0;-webkit-box-sizing:border-box;box-sizing:border-box;cursor:pointer;display:inline-block;max-height:48px;overflow:hidden;outline:none;padding:0;vertical-align:middle;width:134px;-webkit-border-radius:8px;border-radius:8px}.gb\_Wa.gb\_H{background-color:transparent;border:1px solid #5f6368}.gb\_3a{display:inherit}.gb\_Wa.gb\_H .gb\_3a{background:#fff;-webkit-border-radius:4px;border-radius:4px;display:inline-block;left:8px;margin-right:5px;position:relative;padding:3px;top:-1px}.gb\_Wa:hover{border:1px solid #d2e3fc;background-color:rgba(248,250,255,.88)}.gb\_Wa.gb\_H:hover{background-color:rgba(241,243,244,.04);border:1px solid #5f6368}.gb\_Wa:focus-visible,.gb\_Wa:focus{background-color:#fff;outline:1px solid #202124;-webkit-box-shadow:0 1px 2px 0 rgba(60,64,67,.3),0 1px 3px 1px rgba(60,64,67,.15);box-shadow:0 1px 2px 0 rgba(60,64,67,.3),0 1px 3px 1px rgba(60,64,67,.15)}.gb\_Wa.gb\_H:focus-visible,.gb\_Wa.gb\_H:focus{background-color:rgba(241,243,244,.12);outline:1px solid #f1f3f4;-webkit-box-shadow:0 1px 3px 1px rgba(0,0,0,.15),0 1px 2px 0 rgba(0,0,0,.3);box-shadow:0 1px 3px 1px rgba(0,0,0,.15),0 1px 2px 0 rgba(0,0,0,.3)}.gb\_Wa.gb\_H:active,.gb\_Wa.gb\_Uc.gb\_H:focus{background-color:rgba(241,243,244,.1);border:1px solid #5f6368}.gb\_4a{display:inline-block;padding-bottom:2px;padding-left:7px;padding-top:2px;text-align:center;vertical-align:middle;line-height:32px;width:78px}.gb\_Wa.gb\_H .gb\_4a{line-height:26px;margin-left:0;padding-bottom:0;padding-left:0;padding-top:0;width:72px}.gb\_4a.gb\_5a{background-color:#f1f3f4;-webkit-border-radius:4px;border-radius:4px;margin-left:8px;padding-left:0;line-height:30px}.gb\_4a.gb\_5a .gb\_Jc{vertical-align:middle}.gb\_Fa:not(.gb\_cc) .gb\_Wa{margin-left:10px;margin-right:4px}.gb\_Td{max-height:32px;width:78px}.gb\_Wa.gb\_H .gb\_Td{max-height:26px;width:72px}.gb\_P{-webkit-background-size:32px 32px;background-size:32px 32px;border:0;-webkit-border-radius:50%;border-radius:50%;display:block;margin:0px;position:relative;height:32px;width:32px;z-index:0}.gb\_eb{background-color:#e8f0fe;border:1px solid rgba(32,33,36,.08);position:relative}.gb\_eb.gb\_P{height:30px;width:30px}.gb\_eb.gb\_P:hover,.gb\_eb.gb\_P:active{-webkit-box-shadow:none;box-shadow:none}.gb\_fb{background:#fff;border:none;-webkit-border-radius:50%;border-radius:50%;bottom:2px;-webkit-box-shadow:0px 1px 2px 0px rgba(60,64,67,.30),0px 1px 3px 1px rgba(60,64,67,.15);box-shadow:0px 1px 2px 0px rgba(60,64,67,.30),0px 1px 3px 1px rgba(60,64,67,.15);height:14px;margin:2px;position:absolute;right:0;width:14px}.gb\_wc{color:#1f71e7;font:400 22px/32px Google Sans,Roboto,Helvetica,Arial,sans-serif;text-align:center;text-transform:uppercase}@media (-webkit-min-device-pixel-ratio:1.25),(min-resolution:1.25dppx),(min-device-pixel-ratio:1.25){.gb\_P::before,.gb\_gb::before{display:inline-block;-webkit-transform:scale(0.5);-webkit-transform:scale(0.5);transform:scale(0.5);-webkit-transform-origin:left 0;-webkit-transform-origin:left 0;transform-origin:left 0}.gb\_3 .gb\_gb::before{-webkit-transform:scale(scale(0.416666667));-webkit-transform:scale(scale(0.416666667));transform:scale(scale(0.416666667))}}.gb\_P:hover,.gb\_P:focus{-webkit-box-shadow:0 1px 0 rgba(0,0,0,.15);box-shadow:0 1px 0 rgba(0,0,0,.15)}.gb\_P:active{-webkit-box-shadow:inset 0 2px 0 rgba(0,0,0,.15);box-shadow:inset 0 2px 0 rgba(0,0,0,.15)}.gb\_P:active::after{background:rgba(0,0,0,.1);-webkit-border-radius:50%;border-radius:50%;content:"";display:block;height:100%}.gb\_hb{cursor:pointer;line-height:40px;min-width:30px;opacity:.75;overflow:hidden;vertical-align:middle;text-overflow:ellipsis}.gb\_B.gb\_hb{width:auto}.gb\_hb:hover,.gb\_hb:focus{opacity:.85}.gb\_hd .gb\_hb,.gb\_hd .gb\_Wd{line-height:26px}#gb#gb.gb\_hd a.gb\_hb,.gb\_hd .gb\_Wd{font-size:11px;height:auto}.gb\_ib{border-top:4px solid #000;border-left:4px dashed transparent;border-right:4px dashed transparent;display:inline-block;margin-left:6px;opacity:.75;vertical-align:middle}.gb\_Za:hover .gb\_ib{opacity:.85}.gb\_Wa>.gb\_z{padding:3px 3px 3px 4px}.gb\_Xd.gb\_od{color:#fff}.gb\_1 .gb\_hb,.gb\_1 .gb\_ib{opacity:1}#gb#gb.gb\_1.gb\_1 a.gb\_hb,#gb#gb .gb\_1.gb\_1 a.gb\_hb{color:#fff}.gb\_1.gb\_1 .gb\_ib{border-top-color:#fff;opacity:1}.gb\_ka .gb\_P:hover,.gb\_1 .gb\_P:hover,.gb\_ka .gb\_P:focus,.gb\_1 .gb\_P:focus{-webkit-box-shadow:0 1px 0 rgba(0,0,0,.15),0 1px 2px rgba(0,0,0,.2);box-shadow:0 1px 0 rgba(0,0,0,.15),0 1px 2px rgba(0,0,0,.2)}.gb\_Zd .gb\_z,.gb\_0d .gb\_z{position:absolute;right:1px}.gb\_z.gb\_0,.gb\_jb.gb\_0,.gb\_Za.gb\_0{-webkit-flex:0 1 auto;-webkit-box-flex:0;flex:0 1 auto}.gb\_1d.gb\_2d .gb\_hb{width:30px!important}.gb\_3d{height:40px;position:absolute;right:-5px;top:-5px;width:40px}.gb\_4d .gb\_3d,.gb\_5d .gb\_3d{right:0;top:0}.gb\_z .gb\_B{padding:4px}.gb\_S{display:none}sentinel{};this.gbar\_={CONFIG:\[\[\[0,"www.gstatic.com","og.qtm.en\_US.v2pk7dVghog.2019.O","com","en","331",0,\[4,2,"","","","793424555","0"\],null,"VrmgaN\_ePNCx6-AP\_M2mcQ",null,0,"og.qtm.5bOMfS7uCn8.L.W.O","AA2YrTthfa-GW6nWNiVo32au3OStcP0\_zg","AA2YrTs5z5IeveM3\_8fj3UK\_0H1gj7fqJg","",2,1,200,"USA",null,null,"18","331",1,null,null,111881503,null,0,0\],null,\[1,0.1000000014901161,2,1\],null,\[1,0,0,null,"0","nadkarnisanket11@gmail.com","","AIhRldIBdlN2i-JHxfN9h7fE4f15UhZQhDkhuOzFrQWGiaiz639VPS9pp0OB6-13BKj4e2EjnMlD08Q5fQ9n\_fDu7WrNd6Uy0A",0,0,0,""\],\[0,0,"",1,0,0,0,0,0,0,null,0,0,null,0,0,null,null,0,0,0,"","","","","","",null,0,0,0,0,0,null,null,null,"rgba(32,33,36,1)","rgba(255,255,255,1)",0,0,0,null,null,null,0\],\["%1$s (default)","Brand account",1,"%1$s (delegated)",1,null,83,"?authuser=$authuser",null,null,null,1,"https://accounts.google.com/ListAccounts?listPages=0\\u0026authuser=0\\u0026pid=331\\u0026gpsia=1\\u0026source=ogb\\u0026atic=1\\u0026mo=1\\u0026mn=1\\u0026hl=en",0,"dashboard",null,null,null,null,"Profile","",1,null,"Signed out","https://accounts.google.com/AccountChooser?source=ogb\\u0026continue=$continue\\u0026Email=$email\\u0026ec=GAhAywI","https://accounts.google.com/RemoveLocalAccount?source=ogb","Remove","Sign in",0,1,1,0,1,1,0,null,null,null,"Session expired",null,null,null,"Visitor",null,"Default","Delegated","Sign out of all accounts",1,null,null,0,null,null,"myaccount.google.com","https",0,1,0\],null,\["1","gci\_91f30755d6a6b787dcc2a4062e6e9824.js","googleapis.client:gapi.iframes","0","en"\],null,null,null,null,\["m;/\_/scs/abc-static/\_/js/k=gapi.gapi.en.GJa4oir6WlA.O/d=1/rs=AHpOoo-oT18V72om9ubISB9Na8GvbQT5cg/m=\_\_features\_\_","https://apis.google.com","","","1","",null,1,"es\_plusone\_gc\_20250803.0\_p0","en",null,0\],\[0.009999999776482582,"com","331",\[null,"","0",null,1,5184000,null,null,"",null,null,null,null,null,0,null,0,null,1,0,0,0,null,null,0,0,null,0,0,0,0,0\],null,null,null,0\],\[1,null,null,40400,331,"USA","en","793424555.0",8,null,1,0,null,null,null,null,"3700949,105071010,105071012",null,null,null,"VrmgaN\_ePNCx6-AP\_M2mcQ",0,0,0,null,2,5,"nn",182,0,0,null,null,1,111881503,0,0\],\[\[null,null,null,"https://www.gstatic.com/og/\_/js/k=og.qtm.en\_US.v2pk7dVghog.2019.O/rt=j/m=qabr,qgl,q\_dnp,qcwid,qbd,qapid,qads,qrcd,q\_dg/exm=qaaw,qadd,qaid,qein,qhaw,qhba,qhbr,qhch,qhga,qhid,qhin/d=1/ed=1/rs=AA2YrTthfa-GW6nWNiVo32au3OStcP0\_zg"\],\[null,null,null,"https://www.gstatic.com/og/\_/ss/k=og.qtm.5bOMfS7uCn8.L.W.O/m=qcwid,qba/excm=qaaw,qadd,qaid,qein,qhaw,qhba,qhbr,qhch,qhga,qhid,qhin/d=1/ed=1/ct=zgms/rs=AA2YrTs5z5IeveM3\_8fj3UK\_0H1gj7fqJg"\]\],null,null,null,\[\[\[null,null,\[null,null,null,"https://ogs.google.com/u/0/widget/account?amb=1"\],0,414,436,57,4,1,0,0,65,66,8000,"https://accounts.google.com/SignOutOptions?hl=en\\u0026continue=https://cloud.google.com/\_d/profile/ogb\\u0026ec=GBRAywI",68,2,null,null,1,113,"Something went wrong.%1$s Refresh to try again or %2$schoose another account%3$s.",3,null,null,75,0,null,null,null,null,null,null,null,"/widget/account",\["https","myaccount.google.com",0,32,83,0\],0,0,1,\["Critical security alert","Important account alert","Storage usage alert",null,1,0\],0,1,null,1,1,null,null,null,null,0,0,0,null,0,0,null,null,null,null,null,null,null,null,null,0\],\[null,null,\[null,null,null,"https://ogs.google.com/u/0/widget/callout/sid?dc=1"\],null,280,420,70,25,0,null,0,null,null,8000,null,71,4,null,null,null,null,null,null,null,null,76,null,null,null,107,108,109,"",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,0\]\],null,null,"18","331",1,0,null,"en",0,\["?authuser=$authuser","https://accounts.google.com/AddSession?continue=\\u0026ec=GAlAywI","https://accounts.google.com/Logout?continue=https://cloud.google.com/\\u0026service=ahsid\\u0026ec=GAdAywI","https://accounts.google.com/ListAccounts?listPages=0\\u0026authuser=0\\u0026pid=331\\u0026gpsia=1\\u0026source=ogb\\u0026atic=1\\u0026mo=1\\u0026mn=1\\u0026hl=en",0,0,"",0,0,null,0,0,"https://accounts.google.com/ServiceLogin?continue=https://cloud.google.com/\\u0026authuser=0\\u0026ec=GAZAywI",null,null,0,null,null,null,0\],0,0,0,\[null,"",null,null,null,1,null,0,0,"","","","https://ogads-pa.clients6.google.com",0,0,0,"","",0,0,null,86400,null,1,null,null,0,null,0,0,"8559284470",0,0,0\],0,null,null,null,1,0,"nadkarnisanket11@gmail.com",0\],null,\[\["mousedown","touchstart","touchmove","wheel","keydown"\],300000\],\[\[null,null,null,"https://accounts.google.com/RotateCookiesPage"\],3,null,null,null,0,1\]\]\],};this.gbar\_=this.gbar\_||{};(function(\_){var window=this; try{ \_.\_F\_toggles\_initialize=function(a){(typeof globalThis!=="undefined"?globalThis:typeof self!=="undefined"?self:this).\_F\_toggles\_gbar\_=a||\[\]};(0,\_.\_F\_toggles\_initialize)(\[\]); /\* Copyright The Closure Library Authors. SPDX-License-Identifier: Apache-2.0 \*/ var ja,pa,qa,ua,wa,xa,Fa,Ga,$a,cb,eb,jb,fb,lb,rb,Db,Eb,Fb,Gb;\_.aa=function(a,b){if(Error.captureStackTrace)Error.captureStackTrace(this,\_.aa);else{const c=Error().stack;c&&(this.stack=c)}a&&(this.message=String(a));b!==void 0&&(this.cause=b)};\_.ba=function(a){a.zk=!0;return a};\_.ia=function(a){var b=a;if(da(b)){if(!/^\\s\*(?:-?\[1-9\]\\d\*|0)?\\s\*$/.test(b))throw Error(String(b));}else if(ea(b)&&!Number.isSafeInteger(b))throw Error(String(b));return fa?BigInt(a):a=ha(a)?a?"1":"0":da(a)?a.trim()||"0":String(a)}; ja=function(a,b){if(a.length>b.length)return!1;if(a.length<b.length||a===b)return!0;for(let c=0;c<a.length;c++){const d=a\[c\],e=b\[c\];if(d>e)return!1;if(d<e)return!0}};\_.ka=function(a){\_.t.setTimeout(()=>{throw a;},0)};\_.ma=function(){return \_.la().toLowerCase().indexOf("webkit")!=-1};\_.la=function(){var a=\_.t.navigator;return a&&(a=a.userAgent)?a:""};pa=function(a){if(!na||!oa)return!1;for(let b=0;b<oa.brands.length;b++){const {brand:c}=oa.brands\[b\];if(c&&c.indexOf(a)!=-1)return!0}return!1}; \_.u=function(a){return \_.la().indexOf(a)!=-1};qa=function(){return na?!!oa&&oa.brands.length>0:!1};\_.ra=function(){return qa()?!1:\_.u("Opera")};\_.sa=function(){return qa()?!1:\_.u("Trident")||\_.u("MSIE")};\_.ta=function(){return \_.u("Firefox")||\_.u("FxiOS")};\_.va=function(){return \_.u("Safari")&&!(ua()||(qa()?0:\_.u("Coast"))||\_.ra()||(qa()?0:\_.u("Edge"))||(qa()?pa("Microsoft Edge"):\_.u("Edg/"))||(qa()?pa("Opera"):\_.u("OPR"))||\_.ta()||\_.u("Silk")||\_.u("Android"))}; ua=function(){return qa()?pa("Chromium"):(\_.u("Chrome")||\_.u("CriOS"))&&!(qa()?0:\_.u("Edge"))||\_.u("Silk")};wa=function(){return na?!!oa&&!!oa.platform:!1};xa=function(){return \_.u("iPhone")&&!\_.u("iPod")&&!\_.u("iPad")};\_.ya=function(){return xa()||\_.u("iPad")||\_.u("iPod")};\_.za=function(){return wa()?oa.platform==="macOS":\_.u("Macintosh")};\_.Ba=function(a,b){return \_.Aa(a,b)>=0};\_.Ca=function(a,b=!1){return b&&Symbol.for&&a?Symbol.for(a):a!=null?Symbol(a):Symbol()}; \_.Ea=function(a,b){return b===void 0?a.j!==Da&&!!(2&(a.fa\[\_.v\]|0)):!!(2&b)&&a.j!==Da};Fa=function(a){return a};Ga=function(a,b){a.\_\_closure\_\_error\_\_context\_\_984382||(a.\_\_closure\_\_error\_\_context\_\_984382={});a.\_\_closure\_\_error\_\_context\_\_984382.severity=b};\_.Ha=function(a){a=Error(a);Ga(a,"warning");return a};\_.Ja=function(a,b){if(a!=null){var c;var d=(c=Ia)!=null?c:Ia={};c=d\[a\]||0;c>=b||(d\[a\]=c+1,a=Error(),Ga(a,"incident"),\_.ka(a))}}; \_.La=function(a){if(typeof a!=="boolean")throw Error("k\`"+\_.Ka(a)+"\`"+a);return a};\_.Ma=function(a){if(a==null||typeof a==="boolean")return a;if(typeof a==="number")return!!a};\_.Oa=function(a){if(!(0,\_.Na)(a))throw \_.Ha("enum");return a|0};\_.Pa=function(a){return a==null?a:(0,\_.Na)(a)?a|0:void 0};\_.Qa=function(a){if(typeof a!=="number")throw \_.Ha("int32");if(!(0,\_.Na)(a))throw \_.Ha("int32");return a|0};\_.Ra=function(a){if(a!=null&&typeof a!=="string")throw Error();return a}; \_.Sa=function(a){return a==null||typeof a==="string"?a:void 0};\_.Va=function(a,b,c){if(a!=null&&a\[\_.Ta\]===\_.Ua)return a;if(Array.isArray(a)){var d=a\[\_.v\]|0;c=d|c&32|c&2;c!==d&&(a\[\_.v\]=c);return new b(a)}};\_.Ya=function(a){const b=\_.Wa(\_.Xa);return b?a\[b\]:void 0};$a=function(a,b){b<100||\_.Ja(Za,1)}; cb=function(a,b,c,d){const e=d!==void 0;d=!!d;var f=\_.Wa(\_.Xa),g;!e&&f&&(g=a\[f\])&&g.xd($a);f=\[\];var h=a.length;let k;g=4294967295;let l=!1;const m=!!(b&64),p=m?b&128?0:-1:void 0;if(!(b&1||(k=h&&a\[h-1\],k!=null&&typeof k==="object"&&k.constructor===Object?(h--,g=h):k=void 0,!m||b&128||e))){l=!0;var r;g=((r=ab)!=null?r:Fa)(g-p,p,a,k,void 0)+p}b=void 0;for(r=0;r<h;r++){let w=a\[r\];if(w!=null&&(w=c(w,d))!=null)if(m&&r>=g){const D=r-p;var q=void 0;((q=b)!=null?q:b={})\[D\]=w}else f\[r\]=w}if(k)for(let w in k){q= k\[w\];if(q==null||(q=c(q,d))==null)continue;h=+w;let D;if(m&&!Number.isNaN(h)&&(D=h+p)<g)f\[D\]=q;else{let Q;((Q=b)!=null?Q:b={})\[w\]=q}}b&&(l?f.push(b):f\[g\]=b);e&&\_.Wa(\_.Xa)&&(a=\_.Ya(a))&&"function"==typeof \_.bb&&a instanceof \_.bb&&(f\[\_.Xa\]=a.i());return f}; eb=function(a){switch(typeof a){case "number":return Number.isFinite(a)?a:""+a;case "bigint":return(0,\_.db)(a)?Number(a):""+a;case "boolean":return a?1:0;case "object":if(Array.isArray(a)){const b=a\[\_.v\]|0;return a.length===0&&b&1?void 0:cb(a,b,eb)}if(a!=null&&a\[\_.Ta\]===\_.Ua)return fb(a);if("function"==typeof \_.gb&&a instanceof \_.gb)return a.j();return}return a};jb=function(a,b){if(b){ab=b==null||b===Fa||b\[hb\]!==ib?Fa:b;try{return fb(a)}finally{ab=void 0}}return fb(a)}; fb=function(a){a=a.fa;return cb(a,a\[\_.v\]|0,eb)}; \_.mb=function(a,b,c,d=0){if(a==null){var e=32;c?(a=\[c\],e|=128):a=\[\];b&&(e=e&-8380417|(b&1023)<<13)}else{if(!Array.isArray(a))throw Error("l");e=a\[\_.v\]|0;if(kb&&1&e)throw Error("m");2048&e&&!(2&e)&&lb();if(e&256)throw Error("n");if(e&64)return d!==0||e&2048||(a\[\_.v\]=e|2048),a;if(c&&(e|=128,c!==a\[0\]))throw Error("o");a:{c=a;e|=64;var f=c.length;if(f){var g=f-1;const k=c\[g\];if(k!=null&&typeof k==="object"&&k.constructor===Object){b=e&128?0:-1;g-=b;if(g>=1024)throw Error("q");for(var h in k)if(f=+h,f< g)c\[f+b\]=k\[h\],delete k\[h\];else break;e=e&-8380417|(g&1023)<<13;break a}}if(b){h=Math.max(b,f-(e&128?0:-1));if(h>1024)throw Error("r");e=e&-8380417|(h&1023)<<13}}}e|=64;d===0&&(e|=2048);a\[\_.v\]=e;return a};lb=function(){if(kb)throw Error("p");\_.Ja(nb,5)}; rb=function(a,b){if(typeof a!=="object")return a;if(Array.isArray(a)){var c=a\[\_.v\]|0;a.length===0&&c&1?a=void 0:c&2||(!b||4096&c||16&c?a=\_.ob(a,c,!1,b&&!(c&16)):(a\[\_.v\]|=34,c&4&&Object.freeze(a)));return a}if(a!=null&&a\[\_.Ta\]===\_.Ua)return b=a.fa,c=b\[\_.v\]|0,\_.Ea(a,c)?a:\_.pb(a,b,c)?\_.qb(a,b):\_.ob(b,c);if("function"==typeof \_.gb&&a instanceof \_.gb)return a};\_.qb=function(a,b,c){a=new a.constructor(b);c&&(a.j=Da);a.o=Da;return a}; \_.ob=function(a,b,c,d){d!=null||(d=!!(34&b));a=cb(a,b,rb,d);d=32;c&&(d|=2);b=b&8380609|d;a\[\_.v\]=b;return a};\_.tb=function(a){const b=a.fa,c=b\[\_.v\]|0;return \_.Ea(a,c)?\_.pb(a,b,c)?\_.qb(a,b,!0):new a.constructor(\_.ob(b,c,!1)):a};\_.ub=function(a){if(a.j!==Da)return!1;var b=a.fa;b=\_.ob(b,b\[\_.v\]|0);b\[\_.v\]|=2048;a.fa=b;a.j=void 0;a.o=void 0;return!0};\_.vb=function(a){if(!\_.ub(a)&&\_.Ea(a,a.fa\[\_.v\]|0))throw Error();};\_.wb=function(a,b){b===void 0&&(b=a\[\_.v\]|0);b&32&&!(b&4096)&&(a\[\_.v\]=b|4096)}; \_.pb=function(a,b,c){return c&2?!0:c&32&&!(c&4096)?(b\[\_.v\]=c|2,a.j=Da,!0):!1};\_.xb=function(a,b,c,d,e){const f=c+(e?0:-1);var g=a.length-1;if(g>=1+(e?0:-1)&&f>=g){const h=a\[g\];if(h!=null&&typeof h==="object"&&h.constructor===Object)return h\[c\]=d,b}if(f<=g)return a\[f\]=d,b;if(d!==void 0){let h;g=((h=b)!=null?h:b=a\[\_.v\]|0)>>13&1023||536870912;c>=g?d!=null&&(a\[g+(e?0:-1)\]={\[c\]:d}):a\[f\]=d}return b}; \_.zb=function(a,b,c,d,e){let f=!1;d=\_.yb(a,d,e,g=>{const h=\_.Va(g,c,b);f=h!==g&&h!=null;return h});if(d!=null)return f&&!\_.Ea(d)&&\_.wb(a,b),d};\_.Ab=function(){const a=class{constructor(){throw Error();}};Object.setPrototypeOf(a,a.prototype);return a};\_.x=function(a,b){return a!=null?!!a:!!b};\_.y=function(a,b){b==void 0&&(b="");return a!=null?a:b};\_.Bb=function(a,b,c){for(const d in a)b.call(c,a\[d\],d,a)};\_.Cb=function(a){for(const b in a)return!1;return!0};Db=Object.defineProperty; Eb=function(a){a=\["object"==typeof globalThis&&globalThis,a,"object"==typeof window&&window,"object"==typeof self&&self,"object"==typeof global&&global\];for(var b=0;b<a.length;++b){var c=a\[b\];if(c&&c.Math==Math)return c}throw Error("a");};Fb=Eb(this);Gb=function(a,b){if(b)a:{var c=Fb;a=a.split(".");for(var d=0;d<a.length-1;d++){var e=a\[d\];if(!(e in c))break a;c=c\[e\]}a=a\[a.length-1\];d=c\[a\];b=b(d);b!=d&&b!=null&&Db(c,a,{configurable:!0,writable:!0,value:b})}};Gb("globalThis",function(a){return a||Fb}); Gb("Symbol.dispose",function(a){return a?a:Symbol("b")});Gb("Promise.prototype.finally",function(a){return a?a:function(b){return this.then(function(c){return Promise.resolve(b()).then(function(){return c})},function(c){return Promise.resolve(b()).then(function(){throw c;})})}}); Gb("Array.prototype.flat",function(a){return a?a:function(b){b=b===void 0?1:b;var c=\[\];Array.prototype.forEach.call(this,function(d){Array.isArray(d)&&b>0?(d=Array.prototype.flat.call(d,b-1),c.push.apply(c,d)):c.push(d)});return c}});var Jb,Kb,Nb;\_.Hb=\_.Hb||{};\_.t=this||self;Jb=function(a,b){var c=\_.Ib("WIZ\_global\_data.oxN3nb");a=c&&c\[a\];return a!=null?a:b};Kb=\_.t.\_F\_toggles\_gbar\_||\[\];\_.Ib=function(a,b){a=a.split(".");b=b||\_.t;for(var c=0;c<a.length;c++)if(b=b\[a\[c\]\],b==null)return null;return b};\_.Ka=function(a){var b=typeof a;return b!="object"?b:a?Array.isArray(a)?"array":b:"null"};\_.Lb=function(a){var b=typeof a;return b=="object"&&a!=null||b=="function"};\_.Mb="closure\_uid\_"+(Math.random()\*1E9>>>0); Nb=function(a,b,c){return a.call.apply(a.bind,arguments)};\_.z=function(a,b,c){\_.z=Nb;return \_.z.apply(null,arguments)};\_.Ob=function(a,b){var c=Array.prototype.slice.call(arguments,1);return function(){var d=c.slice();d.push.apply(d,arguments);return a.apply(this,d)}};\_.A=function(a,b){a=a.split(".");for(var c=\_.t,d;a.length&&(d=a.shift());)a.length||b===void 0?c\[d\]&&c\[d\]!==Object.prototype\[d\]?c=c\[d\]:c=c\[d\]={}:c\[d\]=b};\_.Wa=function(a){return a}; \_.B=function(a,b){function c(){}c.prototype=b.prototype;a.X=b.prototype;a.prototype=new c;a.prototype.constructor=a;a.nk=function(d,e,f){for(var g=Array(arguments.length-2),h=2;h<arguments.length;h++)g\[h-2\]=arguments\[h\];return b.prototype\[e\].apply(d,g)}};\_.B(\_.aa,Error);\_.aa.prototype.name="CustomError";var Pb=!!(Kb\[0\]>>15&1),Qb=!!(Kb\[0\]&1024),Rb=!!(Kb\[0\]>>16&1),Sb=!!(Kb\[0\]&128);var Tb=Jb(1,!0),na=Pb?Rb:Jb(610401301,!1),kb=Pb?Qb||!Sb:Jb(748402147,Tb);\_.Ub=\_.ba(a=>a!==null&&a!==void 0);var ea=\_.ba(a=>typeof a==="number"),da=\_.ba(a=>typeof a==="string"),ha=\_.ba(a=>typeof a==="boolean");var fa=typeof \_.t.BigInt==="function"&&typeof \_.t.BigInt(0)==="bigint";var Xb,Vb,Yb,Wb;\_.db=\_.ba(a=>fa?a>=Vb&&a<=Wb:a\[0\]==="-"?ja(a,Xb):ja(a,Yb));Xb=Number.MIN\_SAFE\_INTEGER.toString();Vb=fa?BigInt(Number.MIN\_SAFE\_INTEGER):void 0;Yb=Number.MAX\_SAFE\_INTEGER.toString();Wb=fa?BigInt(Number.MAX\_SAFE\_INTEGER):void 0;\_.Zb=typeof TextDecoder!=="undefined";\_.$b=typeof TextEncoder!=="undefined";var oa,ac=\_.t.navigator;oa=ac?ac.userAgentData||null:null;\_.Aa=function(a,b){return Array.prototype.indexOf.call(a,b,void 0)};\_.bc=function(a,b,c){Array.prototype.forEach.call(a,b,c)};\_.cc=function(a,b){return Array.prototype.some.call(a,b,void 0)};\_.dc=function(a){\_.dc\[" "\](a);return a};\_.dc\[" "\]=function(){};var rc;\_.ec=\_.ra();\_.fc=\_.sa();\_.hc=\_.u("Edge");\_.ic=\_.u("Gecko")&&!(\_.ma()&&!\_.u("Edge"))&&!(\_.u("Trident")||\_.u("MSIE"))&&!\_.u("Edge");\_.jc=\_.ma()&&!\_.u("Edge");\_.kc=\_.za();\_.lc=wa()?oa.platform==="Windows":\_.u("Windows");\_.mc=wa()?oa.platform==="Android":\_.u("Android");\_.nc=xa();\_.oc=\_.u("iPad");\_.pc=\_.u("iPod");\_.qc=\_.ya(); a:{let a="";const b=function(){const c=\_.la();if(\_.ic)return/rv:(\[^\\);\]+)(\\)|;)/.exec(c);if(\_.hc)return/Edge\\/(\[\\d\\.\]+)/.exec(c);if(\_.fc)return/\\b(?:MSIE|rv)\[: \](\[^\\);\]+)(\\)|;)/.exec(c);if(\_.jc)return/WebKit\\/(\\S+)/.exec(c);if(\_.ec)return/(?:Version)\[ \\/\]?(\\S+)/.exec(c)}();b&&(a=b?b\[1\]:"");if(\_.fc){var sc;const c=\_.t.document;sc=c?c.documentMode:void 0;if(sc!=null&&sc>parseFloat(a)){rc=String(sc);break a}}rc=a}\_.tc=rc;\_.uc=\_.ta();\_.vc=xa()||\_.u("iPod");\_.wc=\_.u("iPad");\_.xc=\_.u("Android")&&!(ua()||\_.ta()||\_.ra()||\_.u("Silk"));\_.yc=ua();\_.zc=\_.va()&&!\_.ya();var Za,nb,hb;\_.Xa=\_.Ca();\_.Ac=\_.Ca();Za=\_.Ca();\_.Bc=\_.Ca();nb=\_.Ca();\_.Ta=\_.Ca("m\_m",!0);hb=\_.Ca();\_.Cc=\_.Ca();var Ec;\_.v=\_.Ca("jas",!0);Ec=\[\];Ec\[\_.v\]=7;\_.Dc=Object.freeze(Ec);var Da;\_.Ua={};Da={};\_.Fc=Object.freeze({});var ib={};var Ia=void 0;\_.Gc=typeof BigInt==="function"?BigInt.asIntN:void 0;\_.Hc=Number.isSafeInteger;\_.Na=Number.isFinite;\_.Ic=Math.trunc;var ab;\_.Jc=\_.ia(0);\_.Kc={};\_.Lc=function(a,b,c,d,e){b=\_.yb(a.fa,b,c,e);if(b!==null||d&&a.o!==Da)return b};\_.yb=function(a,b,c,d){if(b===-1)return null;const e=b+(c?0:-1),f=a.length-1;let g,h;if(!(f<1+(c?0:-1))){if(e>=f)if(g=a\[f\],g!=null&&typeof g==="object"&&g.constructor===Object)c=g\[b\],h=!0;else if(e===f)c=g;else return;else c=a\[e\];if(d&&c!=null){d=d(c);if(d==null)return d;if(!Object.is(d,c))return h?g\[b\]=d:a\[e\]=d,d}return c}};\_.Mc=function(a,b,c,d){\_.vb(a);const e=a.fa;\_.xb(e,e\[\_.v\]|0,b,c,d);return a}; \_.C=function(a,b,c,d){let e=a.fa,f=e\[\_.v\]|0;b=\_.zb(e,f,b,c,d);if(b==null)return b;f=e\[\_.v\]|0;if(!\_.Ea(a,f)){const g=\_.tb(b);g!==b&&(\_.ub(a)&&(e=a.fa,f=e\[\_.v\]|0),b=g,f=\_.xb(e,f,c,b,d),\_.wb(e,f))}return b};\_.E=function(a,b,c){c==null&&(c=void 0);\_.Mc(a,b,c);c&&!\_.Ea(c)&&\_.wb(a.fa);return a};\_.Nc=function(a,b,c,d){return \_.Pa(\_.Lc(a,b,c,d))};\_.F=function(a,b,c=!1,d){let e;return(e=\_.Ma(\_.Lc(a,b,d)))!=null?e:c};\_.G=function(a,b,c="",d){let e;return(e=\_.Sa(\_.Lc(a,b,d)))!=null?e:c}; \_.I=function(a,b,c){return \_.Sa(\_.Lc(a,b,c,\_.Kc))};\_.J=function(a,b,c,d){return \_.Mc(a,b,c==null?c:\_.La(c),d)};\_.K=function(a,b,c){return \_.Mc(a,b,c==null?c:\_.Qa(c))};\_.L=function(a,b,c,d){return \_.Mc(a,b,\_.Ra(c),d)};\_.N=function(a,b,c,d){return \_.Mc(a,b,c==null?c:\_.Oa(c),d)};\_.O=class{constructor(a,b,c){this.fa=\_.mb(a,b,c)}toJSON(){return jb(this)}wa(a){return JSON.stringify(jb(this,a))}};\_.O.prototype\[\_.Ta\]=\_.Ua;\_.O.prototype.toString=function(){return this.fa.toString()};\_.Oc=\_.Ab();\_.Pc=\_.Ab();\_.Rc=\_.Ab();\_.Sc=Symbol();var Tc=class extends \_.O{constructor(a){super(a)}};\_.Uc=class extends \_.O{constructor(a){super(a)}D(a){return \_.K(this,3,a)}};var Vc=class extends \_.O{constructor(a){super(a)}Wb(a){return \_.L(this,24,a)}};\_.Wc=class extends \_.O{constructor(a){super(a)}};\_.P=function(){this.qa=this.qa;this.Y=this.Y};\_.P.prototype.qa=!1;\_.P.prototype.isDisposed=function(){return this.qa};\_.P.prototype.dispose=function(){this.qa||(this.qa=!0,this.R())};\_.P.prototype\[Symbol.dispose\]=function(){this.dispose()};\_.P.prototype.R=function(){if(this.Y)for(;this.Y.length;)this.Y.shift()()};var Xc=class extends \_.P{constructor(){var a=window;super();this.o=a;this.i=\[\];this.j={}}resolve(a){let b=this.o;a=a.split(".");const c=a.length;for(let d=0;d<c;++d)if(b\[a\[d\]\])b=b\[a\[d\]\];else return null;return b instanceof Function?b:null}tb(){const a=this.i.length,b=this.i,c=\[\];for(let d=0;d<a;++d){const e=b\[d\].i(),f=this.resolve(e);if(f&&f!=this.j\[e\])try{b\[d\].tb(f)}catch(g){}else c.push(b\[d\])}this.i=c.concat(b.slice(a))}};var Zc=class extends \_.P{constructor(){var a=\_.Yc;super();this.o=a;this.A=this.i=null;this.v=0;this.B={};this.j=!1;a=window.navigator.userAgent;a.indexOf("MSIE")>=0&&a.indexOf("Trident")>=0&&(a=/\\b(?:MSIE|rv)\[: \](\[^\\);\]+)(\\)|;)/.exec(a))&&a\[1\]&&parseFloat(a\[1\])<9&&(this.j=!0)}C(a,b){this.i=b;this.A=a;b.preventDefault?b.preventDefault():b.returnValue=!1}};\_.$c=class extends \_.O{constructor(a){super(a)}};var ad=class extends \_.O{constructor(a){super(a)}};var dd;\_.bd=function(a,b,c=98,d=new \_.Uc){if(a.i){const e=new Tc;\_.L(e,1,b.message);\_.L(e,2,b.stack);\_.K(e,3,b.lineNumber);\_.N(e,5,1);\_.E(d,40,e);a.i.log(c,d)}};dd=class{constructor(){var a=cd;this.i=null;\_.F(a,4,!0)}log(a,b,c=new \_.Uc){\_.bd(this,a,98,c)}};var ed,fd;ed=function(a){if(a.o.length>0){var b=a.i!==void 0,c=a.j!==void 0;if(b||c){b=b?a.v:a.A;c=a.o;a.o=\[\];try{\_.bc(c,b,a)}catch(d){console.error(d)}}}};\_.gd=class{constructor(a){this.i=a;this.j=void 0;this.o=\[\]}then(a,b,c){this.o.push(new fd(a,b,c));ed(this)}resolve(a){if(this.i!==void 0||this.j!==void 0)throw Error("v");this.i=a;ed(this)}reject(a){if(this.i!==void 0||this.j!==void 0)throw Error("v");this.j=a;ed(this)}v(a){a.j&&a.j.call(a.i,this.i)}A(a){a.o&&a.o.call(a.i,this.j)}}; fd=class{constructor(a,b,c){this.j=a;this.o=b;this.i=c}};\_.hd=a=>{var b="qc";if(a.qc&&a.hasOwnProperty(b))return a.qc;b=new a;return a.qc=b};\_.R=class{constructor(){this.v=new \_.gd;this.i=new \_.gd;this.D=new \_.gd;this.B=new \_.gd;this.C=new \_.gd;this.A=new \_.gd;this.o=new \_.gd;this.j=new \_.gd;this.F=new \_.gd;this.G=new \_.gd}K(){return this.v}qa(){return this.i}O(){return this.D}M(){return this.B}P(){return this.C}L(){return this.A}Y(){return this.o}J(){return this.j}N(){return this.F}static i(){return \_.hd(\_.R)}};var ld;\_.jd=function(){return \_.C(\_.id,Vc,1)};\_.kd=function(){return \_.C(\_.id,\_.Wc,5)};ld=class extends \_.O{constructor(a){super(a)}};var md;window.gbar\_&&window.gbar\_.CONFIG?md=window.gbar\_.CONFIG\[0\]||{}:md=\[\];\_.id=new ld(md);var cd=\_.C(\_.id,ad,3)||new ad;\_.jd()||new Vc;\_.Yc=new dd;\_.A("gbar\_.\_DumpException",function(a){\_.Yc?\_.Yc.log(a):console.error(a)});\_.nd=new Zc;var pd;\_.qd=function(a,b){var c=\_.od.i();if(a in c.i){if(c.i\[a\]!=b)throw new pd;}else{c.i\[a\]=b;const h=c.j\[a\];if(h)for(let k=0,l=h.length;k<l;k++){b=h\[k\];var d=c.i;delete b.i\[a\];if(\_.Cb(b.i)){for(var e=b.j.length,f=Array(e),g=0;g<e;g++)f\[g\]=d\[b.j\[g\]\];b.o.apply(b.v,f)}}delete c.j\[a\]}};\_.od=class{constructor(){this.i={};this.j={}}static i(){return \_.hd(\_.od)}};\_.rd=class extends \_.aa{constructor(){super()}};pd=class extends \_.rd{};\_.A("gbar.A",\_.gd);\_.gd.prototype.aa=\_.gd.prototype.then;\_.A("gbar.B",\_.R);\_.R.prototype.ba=\_.R.prototype.qa;\_.R.prototype.bb=\_.R.prototype.O;\_.R.prototype.bd=\_.R.prototype.P;\_.R.prototype.bf=\_.R.prototype.K;\_.R.prototype.bg=\_.R.prototype.M;\_.R.prototype.bh=\_.R.prototype.L;\_.R.prototype.bj=\_.R.prototype.Y;\_.R.prototype.bk=\_.R.prototype.J;\_.R.prototype.bl=\_.R.prototype.N;\_.A("gbar.a",\_.R.i());window.gbar&&window.gbar.ap&&window.gbar.ap(window.gbar.a);var sd=new Xc;\_.qd("api",sd); var td=\_.kd()||new \_.Wc,ud=window,vd=\_.y(\_.I(td,8));ud.\_\_PVT=vd;\_.qd("eq",\_.nd); }catch(e){\_.\_DumpException(e)} try{ \_.wd=class extends \_.O{constructor(a){super(a)}}; }catch(e){\_.\_DumpException(e)} try{ var xd=class extends \_.O{constructor(a){super(a)}};var yd=class extends \_.P{constructor(){super();this.j=\[\];this.i=\[\]}o(a,b){this.j.push({features:a,options:b!=null?b:null})}init(a,b,c){window.gapi={};const d=window.\_\_\_jsl={};d.h=\_.y(\_.I(a,1));\_.Ma(\_.Lc(a,12))!=null&&(d.dpo=\_.x(\_.F(a,12)));d.ms=\_.y(\_.I(a,2));d.m=\_.y(\_.I(a,3));d.l=\[\];\_.G(b,1)&&(a=\_.I(b,3))&&this.i.push(a);\_.G(c,1)&&(c=\_.I(c,2))&&this.i.push(c);\_.A("gapi.load",(0,\_.z)(this.o,this));return this}};var zd=\_.C(\_.id,\_.$c,14);if(zd){var Bd=\_.C(\_.id,\_.wd,9)||new \_.wd,Cd=new xd,Dd=new yd;Dd.init(zd,Bd,Cd);\_.qd("gs",Dd)}; }catch(e){\_.\_DumpException(e)} })(this.gbar\_); // Google Inc. this.gbar\_=this.gbar\_||{};(function(\_){var window=this; try{ \_.Ed=function(a,b,c){if(!a.j)if(c instanceof Array)for(var d of c)\_.Ed(a,b,d);else{d=(0,\_.z)(a.C,a,b);const e=a.v+c;a.v++;b.dataset.eqid=e;a.B\[e\]=d;b&&b.addEventListener?b.addEventListener(c,d,!1):b&&b.attachEvent?b.attachEvent("on"+c,d):a.o.log(Error("t\`"+b))}}; }catch(e){\_.\_DumpException(e)} try{ var Fd=document.querySelector(".gb\_J .gb\_B"),Gd=document.querySelector("#gb.gb\_Tc");Fd&&!Gd&&\_.Ed(\_.nd,Fd,"click"); }catch(e){\_.\_DumpException(e)} try{ \_.mh=function(a){if(a.v)return a.v;for(const b in a.i)if(a.i\[b\].ha()&&a.i\[b\].B())return a.i\[b\];return null};\_.nh=function(a,b){a.i\[b.J()\]=b};var oh=new class extends \_.P{constructor(){var a=\_.Yc;super();this.B=a;this.v=null;this.o={};this.C={};this.i={};this.j=null}A(a){this.i\[a\]&&(\_.mh(this)&&\_.mh(this).J()==a||this.i\[a\].P(!0))}Ra(a){this.j=a;for(const b in this.i)this.i\[b\].ha()&&this.i\[b\].Ra(a)}kc(a){return a in this.i?this.i\[a\]:null}};\_.qd("dd",oh); }catch(e){\_.\_DumpException(e)} try{ \_.Fi=function(a,b){return \_.J(a,36,b)}; }catch(e){\_.\_DumpException(e)} try{ var Gi=document.querySelector(".gb\_z .gb\_B"),Hi=document.querySelector("#gb.gb\_Tc");Gi&&!Hi&&\_.Ed(\_.nd,Gi,"click"); }catch(e){\_.\_DumpException(e)} })(this.gbar\_); // Google Inc. this.gbar\_=this.gbar\_||{};(function(\_){var window=this; try{ var Id;Id=class extends \_.rd{};\_.Jd=function(a,b){if(b in a.i)return a.i\[b\];throw new Id;};\_.Kd=function(a){return \_.Jd(\_.od.i(),a)}; }catch(e){\_.\_DumpException(e)} try{ /\* Copyright Google LLC SPDX-License-Identifier: Apache-2.0 \*/ var Nd;\_.Ld=function(a){const b=a.length;if(b>0){const c=Array(b);for(let d=0;d<b;d++)c\[d\]=a\[d\];return c}return\[\]};Nd=function(a){return new \_.Md(b=>b.substr(0,a.length+1).toLowerCase()===a+":")};\_.Od=globalThis.trustedTypes;\_.Pd=class{constructor(a){this.i=a}toString(){return this.i}};\_.Qd=new \_.Pd("about:invalid#zClosurez");\_.Md=class{constructor(a){this.Th=a}};\_.Rd=\[Nd("data"),Nd("http"),Nd("https"),Nd("mailto"),Nd("ftp"),new \_.Md(a=>/^\[^:\]\*(\[/?#\]|$)/.test(a))\];\_.Sd=class{constructor(a){this.i=a}toString(){return this.i+""}};\_.Td=new \_.Sd(\_.Od?\_.Od.emptyHTML:""); }catch(e){\_.\_DumpException(e)} try{ var Xd,ie,Wd,Yd,ce;\_.Ud=function(a){if(a==null)return a;if(typeof a==="string"&&a)a=+a;else if(typeof a!=="number")return;return(0,\_.Na)(a)?a|0:void 0};\_.Vd=function(a,b){return a.lastIndexOf(b,0)==0};Xd=function(){let a=null;if(!Wd)return a;try{const b=c=>c;a=Wd.createPolicy("ogb-qtm#html",{createHTML:b,createScript:b,createScriptURL:b})}catch(b){}return a};\_.Zd=function(){Yd===void 0&&(Yd=Xd());return Yd};\_.ae=function(a){const b=\_.Zd();a=b?b.createScriptURL(a):a;return new \_.$d(a)}; \_.be=function(a){if(a instanceof \_.$d)return a.i;throw Error("x");};\_.de=function(a){if(ce.test(a))return a};\_.ee=function(a){if(a instanceof \_.Pd)if(a instanceof \_.Pd)a=a.i;else throw Error("x");else a=\_.de(a);return a};\_.fe=function(a,b=document){let c;const d=(c=b.querySelector)==null?void 0:c.call(b,\`${a}\[nonce\]\`);return d==null?"":d.nonce||d.getAttribute("nonce")||""};\_.S=function(a,b,c){return \_.Ma(\_.Lc(a,b,c,\_.Kc))};\_.ge=function(a,b){return \_.Ud(\_.Lc(a,b,void 0,\_.Kc))}; \_.he=function(a){var b=\_.Ka(a);return b=="array"||b=="object"&&typeof a.length=="number"};Wd=\_.Od;\_.$d=class{constructor(a){this.i=a}toString(){return this.i+""}};ce=/^\\s\*(?!javascript:)(?:\[\\w+.-\]+:|\[^:/?#\]\*(?:\[/?#\]|$))/i;var oe,se,je;\_.le=function(a){return a?new je(\_.ke(a)):ie||(ie=new je)};\_.me=function(a,b){return typeof b==="string"?a.getElementById(b):b};\_.T=function(a,b){var c=b||document;c.getElementsByClassName?a=c.getElementsByClassName(a)\[0\]:(c=document,a=a?(b||c).querySelector(a?"."+a:""):\_.ne(c,"\*",a,b)\[0\]||null);return a||null};\_.ne=function(a,b,c,d){a=d||a;return(b=b&&b!="\*"?String(b).toUpperCase():"")||c?a.querySelectorAll(b+(c?"."+c:"")):a.getElementsByTagName("\*")}; \_.pe=function(a,b){\_.Bb(b,function(c,d){d=="style"?a.style.cssText=c:d=="class"?a.className=c:d=="for"?a.htmlFor=c:oe.hasOwnProperty(d)?a.setAttribute(oe\[d\],c):\_.Vd(d,"aria-")||\_.Vd(d,"data-")?a.setAttribute(d,c):a\[d\]=c})};oe={cellpadding:"cellPadding",cellspacing:"cellSpacing",colspan:"colSpan",frameborder:"frameBorder",height:"height",maxlength:"maxLength",nonce:"nonce",role:"role",rowspan:"rowSpan",type:"type",usemap:"useMap",valign:"vAlign",width:"width"}; \_.qe=function(a){return a?a.defaultView:window};\_.te=function(a,b){const c=b\[1\],d=\_.re(a,String(b\[0\]));c&&(typeof c==="string"?d.className=c:Array.isArray(c)?d.className=c.join(" "):\_.pe(d,c));b.length>2&&se(a,d,b);return d};se=function(a,b,c){function d(e){e&&b.appendChild(typeof e==="string"?a.createTextNode(e):e)}for(let e=2;e<c.length;e++){const f=c\[e\];!\_.he(f)||\_.Lb(f)&&f.nodeType>0?d(f):\_.bc(f&&typeof f.length=="number"&&typeof f.item=="function"?\_.Ld(f):f,d)}}; \_.ue=function(a){return \_.re(document,a)};\_.re=function(a,b){b=String(b);a.contentType==="application/xhtml+xml"&&(b=b.toLowerCase());return a.createElement(b)};\_.ve=function(a){let b;for(;b=a.firstChild;)a.removeChild(b)};\_.we=function(a){return a&&a.parentNode?a.parentNode.removeChild(a):null};\_.xe=function(a,b){return a&&b?a==b||a.contains(b):!1};\_.ke=function(a){return a.nodeType==9?a:a.ownerDocument||a.document};je=function(a){this.i=a||\_.t.document||document};\_.n=je.prototype; \_.n.H=function(a){return \_.me(this.i,a)};\_.n.Pa=function(a,b,c){return \_.te(this.i,arguments)};\_.n.appendChild=function(a,b){a.appendChild(b)};\_.n.Je=\_.ve;\_.n.ng=\_.we;\_.n.mg=\_.xe; }catch(e){\_.\_DumpException(e)} try{ \_.Mi=function(a){const b=\_.fe("script",a.ownerDocument);b&&a.setAttribute("nonce",b)};\_.Ni=function(a){if(!a)return null;a=\_.I(a,4);var b;a===null||a===void 0?b=null:b=\_.ae(a);return b};\_.Oi=function(a,b,c){a=a.fa;return \_.zb(a,a\[\_.v\]|0,b,c)!==void 0};\_.Pi=class extends \_.O{constructor(a){super(a)}};\_.Qi=function(a,b){return(b||document).getElementsByTagName(String(a))}; }catch(e){\_.\_DumpException(e)} try{ var Si=function(a,b,c){a<b?Ri(a+1,b):\_.Yc.log(Error("W\`"+a+"\`"+b),{url:c})},Ri=function(a,b){if(Ti){const c=\_.ue("SCRIPT");c.async=!0;c.type="text/javascript";c.charset="UTF-8";c.src=\_.be(Ti);\_.Mi(c);c.onerror=\_.Ob(Si,a,b,c.src);\_.Qi("HEAD")\[0\].appendChild(c)}},Ui=class extends \_.O{constructor(a){super(a)}};var Vi=\_.C(\_.id,Ui,17)||new Ui,Wi,Ti=(Wi=\_.C(Vi,\_.Pi,1))?\_.Ni(Wi):null,Xi,Yi=(Xi=\_.C(Vi,\_.Pi,2))?\_.Ni(Xi):null,Zi=function(){Ri(1,2);if(Yi){const a=\_.ue("LINK");a.setAttribute("type","text/css");a.href=\_.be(Yi).toString();a.rel="stylesheet";let b=\_.fe("style",document);b&&a.setAttribute("nonce",b);\_.Qi("HEAD")\[0\].appendChild(a)}};(function(){const a=\_.jd();if(\_.S(a,18))Zi();else{const b=\_.ge(a,19)||0;window.addEventListener("load",()=>{window.setTimeout(Zi,b)})}})(); }catch(e){\_.\_DumpException(e)} })(this.gbar\_); // Google Inc.  [Skip to main content](#main-content)

[![Google Cloud](https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/images/cloud-logo.svg)](/)

[Documentation](https://cloud.google.com/docs) [Technology areas](https://cloud.google.com/docs/tech-area-overviews)

close

*   [
    
    AI and ML
    
    ](https://cloud.google.com/docs/ai-ml)
*   [
    
    Application development
    
    ](https://cloud.google.com/docs/application-development)
*   [
    
    Application hosting
    
    ](https://cloud.google.com/docs/application-hosting)
*   [
    
    Compute
    
    ](https://cloud.google.com/docs/compute-area)
*   [
    
    Data analytics and pipelines
    
    ](https://cloud.google.com/docs/data)
*   [
    
    Databases
    
    ](https://cloud.google.com/docs/databases)
*   [
    
    Distributed, hybrid, and multicloud
    
    ](https://cloud.google.com/docs/dhm-cloud)
*   [
    
    Generative AI
    
    ](https://cloud.google.com/docs/generative-ai)
*   [
    
    Industry solutions
    
    ](https://cloud.google.com/docs/industry)
*   [
    
    Networking
    
    ](https://cloud.google.com/docs/networking)
*   [
    
    Observability and monitoring
    
    ](https://cloud.google.com/docs/observability)
*   [
    
    Security
    
    ](https://cloud.google.com/docs/security)
*   [
    
    Storage
    
    ](https://cloud.google.com/docs/storage)

[Cross-product tools](https://cloud.google.com/docs/cross-product-overviews)

close

*   [
    
    Access and resources management
    
    ](https://cloud.google.com/docs/access-resources)
*   [
    
    Costs and usage management
    
    ](https://cloud.google.com/docs/costs-usage)
*   [
    
    Google Cloud SDK, languages, frameworks, and tools
    
    ](https://cloud.google.com/docs/devtools)
*   [
    
    Infrastructure as code
    
    ](https://cloud.google.com/docs/iac)
*   [
    
    Migration
    
    ](https://cloud.google.com/docs/migration)

[Related sites](https://cloud.google.com/)

close

*   [
    
    Google Cloud Home
    
    ](https://cloud.google.com/)
*   [
    
    Free Trial and Free Tier
    
    ](https://cloud.google.com/free)
*   [
    
    Architecture Center
    
    ](https://cloud.google.com/architecture)
*   [
    
    Blog
    
    ](https://cloud.google.com/blog)
*   [
    
    Contact Sales
    
    ](https://cloud.google.com/contact)
*   [
    
    Google Cloud Developer Center
    
    ](https://cloud.google.com/developers)
*   [
    
    Google Developer Center
    
    ](https://developers.google.com/)
*   [
    
    Google Cloud Marketplace
    
    ](https://console.cloud.google.com/marketplace)
*   [
    
    Google Cloud Marketplace Documentation
    
    ](https://cloud.google.com/marketplace/docs)
*   [
    
    Google Cloud Skills Boost
    
    ](https://www.cloudskillsboost.google/paths)
*   [
    
    Google Cloud Solution Center
    
    ](https://cloud.google.com/solutions)
*   [
    
    Google Cloud Support
    
    ](https://cloud.google.com/support-hub)
*   [
    
    Google Cloud Tech Youtube Channel
    
    ](https://www.youtube.com/@googlecloudtech)

More

/

*   [English](https://cloud.google.com/bigquery/docs/clustered-tables)
*   [Deutsch](https://cloud.google.com/bigquery/docs/clustered-tables?hl=de)
*   [Español – América Latina](https://cloud.google.com/bigquery/docs/clustered-tables?hl=es-419)
*   [Français](https://cloud.google.com/bigquery/docs/clustered-tables?hl=fr)
*   [Indonesia](https://cloud.google.com/bigquery/docs/clustered-tables?hl=id)
*   [Italiano](https://cloud.google.com/bigquery/docs/clustered-tables?hl=it)
*   [Português – Brasil](https://cloud.google.com/bigquery/docs/clustered-tables?hl=pt-br)
*   [中文 – 简体](https://cloud.google.com/bigquery/docs/clustered-tables?hl=zh-cn)
*   [中文 – 繁體](https://cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)
*   [日本語](https://cloud.google.com/bigquery/docs/clustered-tables?hl=ja)
*   [한국어](https://cloud.google.com/bigquery/docs/clustered-tables?hl=ko)

[Console](//console.cloud.google.com/)

Google Developer ProgramView your saved pages and finish your Google Developer Profile setup here.

[

![](https://lh3.google.com/u/0/ogw/AF2bZyjkOrwzv87BjtxjPeImvYSOf1dsRjib1R8E_kkK8_jDBA=s32-c-mo)

](https://accounts.google.com/SignOutOptions?hl=en&continue=https%3A%2F%2Fcloud.google.com%2Fbigquery%2Fdocs%2Fclustered-tables&ec=GBRAywI)

*   [BigQuery](https://cloud.google.com/bigquery)

[Guides](https://cloud.google.com/bigquery/docs/introduction) [Reference](https://cloud.google.com/bigquery/quotas) [Samples](https://cloud.google.com/bigquery/docs/samples) [Resources](https://cloud.google.com/bigquery/docs/release-notes) More

[Contact Us](https://cloud.google.com/contact) [Start free](//console.cloud.google.com/freetrial)

[![Google Cloud](https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/images/cloud-logo.svg)](/)

*   [Documentation](/docs)
    *   [Guides](/bigquery/docs/introduction)
    *   [Reference](/bigquery/quotas)
    *   [Samples](/bigquery/docs/samples)
    *   [Resources](/bigquery/docs/release-notes)
*   [Technology areas](/docs/tech-area-overviews)
    *   More
*   [Cross-product tools](/docs/cross-product-overviews)
    *   More
*   [Related sites](/)
    *   More
*   [Console](//console.cloud.google.com/)
*   [Contact Us](/contact)
*   [Start free](//console.cloud.google.com/freetrial)

*   Discover
    
*   [Product overview](/bigquery/docs/introduction)
*   How does BigQuery work?
    
    *   [Storage](/bigquery/docs/storage_overview)
    *   [Analytics](/bigquery/docs/query-overview)
    *   [Administration](/bigquery/docs/admin-intro)
    
*   Get started
    
*   [Use the BigQuery sandbox](/bigquery/docs/sandbox)
*   Quickstarts
    
    *   Try the Cloud console
        
        *   [Query public data](/bigquery/docs/quickstarts/query-public-dataset-console)
        *   [Load and query data](/bigquery/docs/quickstarts/load-data-console)
        
    *   Try the command-line tool
        
        *   [Query public data](/bigquery/docs/quickstarts/query-public-dataset-bq)
        *   [Load and query data](/bigquery/docs/quickstarts/load-data-bq)
        
    *   [Try the client libraries](/bigquery/docs/quickstarts/quickstart-client-libraries)
    *   [Try DataFrames](/bigquery/docs/dataframes-quickstart)
    
*   Explore BigQuery tools
    
    *   [Explore the console](/bigquery/docs/bigquery-web-ui)
    *   [Explore the command-line tool](/bigquery/docs/bq-command-line-tool)
    
*   Migrate
    
*   [Overview](/bigquery/docs/migration/migration-overview)
*   Migrate a data warehouse
    
    *   [Introduction to BigQuery Migration Service](/bigquery/docs/migration-intro)
    *   [Migration assessment](/bigquery/docs/migration-assessment)
    *   [Migrate schema and data](/bigquery/docs/migration/schema-data-overview)
    *   [Migrate data pipelines](/bigquery/docs/migration/pipelines)
    *   Migrate SQL
        
        *   [Translate SQL queries interactively](/bigquery/docs/interactive-sql-translator)
        *   [Translate SQL queries using the API](/bigquery/docs/api-sql-translator)
        *   [Translate SQL queries in batch](/bigquery/docs/batch-sql-translator)
        *   [Generate metadata for translation and assessment](/bigquery/docs/generate-metadata)
        *   [Transform SQL translations with YAML](/bigquery/docs/config-yaml-translation)
        *   [Map SQL object names for batch translation](/bigquery/docs/output-name-mapping)
        
    
*   Migration guides
    
    *   Amazon Redshift
        
        *   [Migration overview](/bigquery/docs/migration/redshift-overview)
        *   [Migrate Amazon Redshift schema and data](/bigquery/docs/migration/redshift)
        *   [Migrate Amazon Redshift schema and data when using a VPC](/bigquery/docs/migration/redshift-vpc)
        *   [SQL translation reference](/bigquery/docs/migration/redshift-sql)
        
    *   Apache Hadoop
        
        *   [Extract metadata from Hadoop for migration](/bigquery/docs/hadoop-metadata)
        *   [Migrate permissions from Hadoop](/bigquery/docs/hadoop-permissions-migration)
        *   [Schedule an HDFS data lake transfer](/bigquery/docs/hdfs-data-lake-transfer)
        
    *   Apache Hive
        
        *   [Hive migration overview](/bigquery/docs/migration/hive-overview)
        *   [Migrate Apache Hive schema and data](/bigquery/docs/migration/hive)
        *   [SQL translation reference](/bigquery/docs/migration/hive-sql)
        
    *   IBM Netezza
        
        *   [Migrate from IBM Netezza](/bigquery/docs/migration/netezza)
        *   [SQL translation reference](/bigquery/docs/migration/netezza-sql)
        
    *   Oracle
        
        *   [Migration guide](/bigquery/docs/migration/oracle-migration)
        *   [SQL translation reference](/bigquery/docs/migration/oracle-sql)
        
    *   Snowflake
        
        *   [Introduction](/bigquery/docs/migration/snowflake-migration-intro)
        *   [Schedule a Snowflake transfer](/bigquery/docs/migration/snowflake-transfer)
        *   [Migration overview](/bigquery/docs/migration/snowflake-overview)
        *   [SQL translation reference](/bigquery/docs/migration/snowflake-sql)
        
    *   Teradata
        
        *   [Introduction](/bigquery/docs/migration/teradata-migration-intro)
        *   [Migration overview](/bigquery/docs/migration/teradata-overview)
        *   [Migrate Teradata schema and data](/bigquery/docs/migration/teradata)
        *   [Migration tutorial](/bigquery/docs/migration/teradata-tutorial)
        *   [SQL translation reference](/bigquery/docs/migration/teradata-sql)
        
    
*   Design
    
*   [Organize resources](/bigquery/docs/resource-hierarchy)
*   [API dependencies](/bigquery/docs/service-dependencies)
*   [Understand editions](/bigquery/docs/editions-intro)
*   Datasets
    
    *   [Introduction](/bigquery/docs/datasets-intro)
    *   [Create datasets](/bigquery/docs/datasets)
    *   [List datasets](/bigquery/docs/listing-datasets)
    *   [Cross-region replication](/bigquery/docs/data-replication)
    *   [Managed disaster recovery](/bigquery/docs/managed-disaster-recovery)
    *   [Migrate to managed disaster recovery](/bigquery/docs/disaster-recovery-migration)
    *   [Dataset data retention](/bigquery/docs/time-travel)
    
*   Tables
    
    *   BigQuery tables
        
        *   [Introduction](/bigquery/docs/tables-intro)
        *   [Create and use tables](/bigquery/docs/tables)
        *   [BigLake Iceberg tables in BigQuery](/bigquery/docs/iceberg-tables)
        *   Specify table schemas
            
            *   [Specify a schema](/bigquery/docs/schemas)
            *   [Specify nested and repeated columns](/bigquery/docs/nested-repeated)
            *   [Specify default column values](/bigquery/docs/default-values)
            *   [Specify ObjectRef values](/bigquery/docs/objectref-columns)
            
        *   Segment with partitioned tables
            
            *   [Introduction](/bigquery/docs/partitioned-tables)
            *   [Create partitioned tables](/bigquery/docs/creating-partitioned-tables)
            *   [Manage partitioned tables](/bigquery/docs/managing-partitioned-tables)
            *   [Query partitioned tables](/bigquery/docs/querying-partitioned-tables)
            
        *   Optimize with clustered tables
            
            *   [Introduction](/bigquery/docs/clustered-tables)
            *   [Create clustered tables](/bigquery/docs/creating-clustered-tables)
            *   [Manage clustered tables](/bigquery/docs/manage-clustered-tables)
            *   [Query clustered tables](/bigquery/docs/querying-clustered-tables)
            
        *   [Use metadata indexing](/bigquery/docs/metadata-indexing-managed-tables)
        
    *   External tables
        
        *   [Introduction](/bigquery/docs/external-data-sources)
        *   Types of external tables
            
            *   [BigLake external tables](/bigquery/docs/biglake-intro)
            *   [BigQuery Omni](/bigquery/docs/omni-introduction)
            *   [Object tables](/bigquery/docs/object-table-introduction)
            *   [External tables](/bigquery/docs/external-tables)
            
        *   [External table definition file](/bigquery/docs/external-table-definition)
        *   [Externally partitioned data](/bigquery/docs/hive-partitioned-queries)
        *   [Use metadata caching](/bigquery/docs/metadata-caching-external-tables)
        *   [Amazon S3 BigLake external tables](/bigquery/docs/omni-aws-create-external-table)
        *   [Apache Iceberg external tables](/bigquery/docs/iceberg-external-tables)
        *   [Azure Blob Storage BigLake tables](/bigquery/docs/omni-azure-create-external-table)
        *   [Bigtable external table](/bigquery/docs/create-bigtable-external-table)
        *   [BigLake external tables for Cloud Storage](/bigquery/docs/create-cloud-storage-table-biglake)
        *   [Cloud Storage object tables](/bigquery/docs/object-tables)
        *   [Cloud Storage external tables](/bigquery/docs/external-data-cloud-storage)
        *   [Delta Lake BigLake tables](/bigquery/docs/create-delta-lake-table)
        *   [Google Drive external tables](/bigquery/docs/external-data-drive)
        
    
*   Views
    
    *   Logical views
        
        *   [Introduction](/bigquery/docs/views-intro)
        *   [Create logical views](/bigquery/docs/views)
        
    *   Materialized views
        
        *   [Introduction](/bigquery/docs/materialized-views-intro)
        *   [Create materialized views](/bigquery/docs/materialized-views-create)
        *   [Create materialized view replicas](/bigquery/docs/materialized-view-replicas-create)
        
    *   Manage all view types
        
        *   [Get information about views](/bigquery/docs/view-metadata)
        *   [Manage views](/bigquery/docs/managing-views)
        
    
*   Routines
    
    *   [Introduction](/bigquery/docs/routines-intro)
    *   [Manage routines](/bigquery/docs/routines)
    *   [User-defined functions](/bigquery/docs/user-defined-functions)
    *   [User-defined functions in Python](/bigquery/docs/user-defined-functions-python)
    *   [User-defined aggregate functions](/bigquery/docs/user-defined-aggregates)
    *   [Table functions](/bigquery/docs/table-functions)
    *   [Remote functions](/bigquery/docs/remote-functions)
    *   [SQL stored procedures](/bigquery/docs/procedures)
    *   [Stored procedures for Apache Spark](/bigquery/docs/spark-procedures)
    *   [Analyze object tables by using remote functions](/bigquery/docs/object-table-remote-function)
    *   [Remote functions and Translation API tutorial](/bigquery/docs/remote-functions-translation-tutorial)
    
*   Connections
    
    *   [Introduction](/bigquery/docs/connections-api-intro)
    *   [Amazon S3 connection](/bigquery/docs/omni-aws-create-connection)
    *   [Apache Spark connection](/bigquery/docs/connect-to-spark)
    *   [Azure Blob Storage connection](/bigquery/docs/omni-azure-create-connection)
    *   [Cloud resource connection](/bigquery/docs/create-cloud-resource-connection)
    *   [Spanner connection](/bigquery/docs/connect-to-spanner)
    *   [Cloud SQL connection](/bigquery/docs/connect-to-sql)
    *   [AlloyDB connection](/bigquery/docs/connect-to-alloydb)
    *   [SAP Datasphere connection](/bigquery/docs/connect-to-sap-datasphere)
    *   [Manage connections](/bigquery/docs/working-with-connections)
    *   [Configure connections with network attachments](/bigquery/docs/connections-with-network-attachment)
    *   [Default connections](/bigquery/docs/default-connections)
    
*   Indexes
    
    *   Search indexes
        
        *   [Introduction](/bigquery/docs/search-intro)
        *   [Manage search indexes](/bigquery/docs/search-index)
        
    *   Vector indexes
        
        *   [Introduction](/bigquery/docs/vector-search-intro)
        *   [Manage vector indexes](/bigquery/docs/vector-index)
        
    
*   Load, transform, and export
    
*   [Introduction](/bigquery/docs/load-transform-export-intro)
*   Load data
    
    *   [Introduction](/bigquery/docs/loading-data)
    *   BigQuery Data Transfer Service
        
        *   [Introduction](/bigquery/docs/dts-introduction)
        *   [Data location and transfers](/bigquery/docs/dts-locations)
        *   [Authorize transfers](/bigquery/docs/dts-authentication-authorization)
        *   [Enable transfers](/bigquery/docs/enable-transfer-service)
        *   Set up network connections
            
            *   [Cloud SQL instance access](/bigquery/docs/cloud-sql-instance-access)
            *   [AWS VPN and network attachment](/bigquery/docs/aws-vpn-network-attachment)
            *   [Azure VPN and network attachment](/bigquery/docs/azure-vpn-network-attachment)
            
        *   [Manage transfers](/bigquery/docs/working-with-transfers)
        *   [Transfer run notifications](/bigquery/docs/transfer-run-notifications)
        *   [Troubleshoot transfer configurations](/bigquery/docs/transfer-troubleshooting)
        *   [Use service accounts](/bigquery/docs/use-service-accounts)
        *   [Use third-party transfers](/bigquery/docs/third-party-transfer)
        *   [Use custom organization policies](/bigquery/docs/transfer-custom-constraints)
        *   [Data source change log](/bigquery/docs/transfer-changes)
        *   [Event-driven transfers](/bigquery/docs/event-driven-transfer)
        *   Transfer guides
            
            *   Amazon S3
                
                *   [Introduction](/bigquery/docs/s3-transfer-intro)
                *   [Schedule transfers](/bigquery/docs/s3-transfer)
                *   [Transfer runtime parameters](/bigquery/docs/s3-transfer-parameters)
                
            *   Azure Blob Storage
                
                *   [Introduction](/bigquery/docs/blob-storage-transfer-intro)
                *   [Schedule transfers](/bigquery/docs/blob-storage-transfer)
                *   [Transfer runtime parameters](/bigquery/docs/blob-storage-transfer-parameters)
                
            *   Campaign Manager
                
                *   [Schedule transfers](/bigquery/docs/doubleclick-campaign-transfer)
                *   [Report transformation](/bigquery/docs/doubleclick-campaign-transformation)
                
            *   Cloud Storage
                
                *   [Introduction](/bigquery/docs/cloud-storage-transfer-overview)
                *   [Schedule transfers](/bigquery/docs/cloud-storage-transfer)
                *   [Transfer runtime parameters](/bigquery/docs/gcs-transfer-parameters)
                
            *   Comparison Shopping Service Center
                
                *   [Introduction](/bigquery/docs/css-center-transfer)
                *   [Schedule transfers](/bigquery/docs/css-center-transfer-schedule-transfers)
                *   [Transfer report schema](/bigquery/docs/css-center-products-schema)
                
            *   Display & Video 360
                
                *   [Schedule transfers](/bigquery/docs/display-video-transfer)
                *   [Report transformation](/bigquery/docs/display-video-transformation)
                
            *   Facebook Ads
                
                *   [Schedule transfers](/bigquery/docs/facebook-ads-transfer)
                *   [Report transformation](/bigquery/docs/facebook-ads-transformation)
                
            *   Google Ad Manager
                
                *   [Schedule transfers](/bigquery/docs/doubleclick-publisher-transfer)
                *   [Report transformation](/bigquery/docs/doubleclick-publisher-transformation)
                
            *   Google Ads
                
                *   [Schedule transfers](/bigquery/docs/google-ads-transfer)
                *   [Report transformation](/bigquery/docs/google-ads-transformation)
                
            *   Google Analytics 4
                
                *   [Schedule transfers](/bigquery/docs/google-analytics-4-transfer)
                *   [Report transformation](/bigquery/docs/google-analytics-4-transformation)
                
            *   Google Merchant Center
                
                *   [Introduction](/bigquery/docs/merchant-center-transfer)
                *   [Schedule transfers](/bigquery/docs/merchant-center-transfer-schedule-transfers)
                *   [Query your data](/bigquery/docs/merchant-center-query-your-data)
                *   Migration guides
                    
                    *   [Best sellers](/bigquery/docs/merchant-center-best-sellers-migration)
                    *   [Price competitiveness](/bigquery/docs/merchant-center-price-competitiveness-migration)
                    
                *   Transfer report schema
                    
                    *   [Best Sellers table](/bigquery/docs/merchant-center-best-sellers-schema)
                    *   [Local Inventories table](/bigquery/docs/merchant-center-local-inventories-schema)
                    *   [Performance table](/bigquery/docs/merchant-center-performance-schema)
                    *   [Price Benchmarks table](/bigquery/docs/merchant-center-price-benchmarks-schema)
                    *   [Price Competitiveness table](/bigquery/docs/merchant-center-price-competitiveness-schema)
                    *   [Price Insights table](/bigquery/docs/merchant-center-price-insights-schema)
                    *   [Product Inventory table](/bigquery/docs/merchant-center-product-inventory-schema)
                    *   [Product Targeting table](/bigquery/docs/merchant-center-product-targeting-schema)
                    *   [Products table](/bigquery/docs/merchant-center-products-schema)
                    *   [Regional Inventories table](/bigquery/docs/merchant-center-regional-inventories-schema)
                    *   [Top Brands table](/bigquery/docs/merchant-center-top-brands-schema)
                    *   [Top Products table](/bigquery/docs/merchant-center-top-products-schema)
                    
                
            *   Google Play
                
                *   [Schedule transfers](/bigquery/docs/play-transfer)
                *   [Transfer report transformation](/bigquery/docs/play-transformation)
                
            *   MySQL
                
                *   [Schedule transfers](/bigquery/docs/mysql-transfer)
                
            *   Oracle
                
                *   [Schedule transfers](/bigquery/docs/oracle-transfer)
                
            *   PostgreSQL
                
                *   [Schedule transfers](/bigquery/docs/postgresql-transfer)
                
            *   Salesforce
                
                *   [Schedule transfers](/bigquery/docs/salesforce-transfer)
                
            *   Salesforce Marketing Cloud
                
                *   [Schedule transfers](/bigquery/docs/sfmc-transfer)
                
            *   Search Ads 360
                
                *   [Schedule transfers](/bigquery/docs/search-ads-transfer)
                *   [Transfer report transformation](/bigquery/docs/search-ads-transformation)
                *   [Migration guide](/bigquery/docs/search-ads-migration-guide)
                
            *   ServiceNow
                
                *   [Schedule transfers](/bigquery/docs/servicenow-transfer)
                
            *   YouTube channel
                
                *   [Schedule transfers](/bigquery/docs/youtube-channel-transfer)
                *   [Transfer report transformation](/bigquery/docs/youtube-channel-transformation)
                
            *   YouTube content owner
                
                *   [Schedule transfers](/bigquery/docs/youtube-content-owner-transfer)
                *   [Transfer report transformation](/bigquery/docs/youtube-content-owner-transformation)
                
            
        
    *   Batch load data
        
        *   [Introduction](/bigquery/docs/batch-loading-data)
        *   [Auto-detect schemas](/bigquery/docs/schema-detect)
        *   [Load Avro data](/bigquery/docs/loading-data-cloud-storage-avro)
        *   [Load Parquet data](/bigquery/docs/loading-data-cloud-storage-parquet)
        *   [Load ORC data](/bigquery/docs/loading-data-cloud-storage-orc)
        *   [Load CSV data](/bigquery/docs/loading-data-cloud-storage-csv)
        *   [Load JSON data](/bigquery/docs/loading-data-cloud-storage-json)
        *   [Load externally partitioned data](/bigquery/docs/hive-partitioned-loads-gcs)
        *   [Load data from a Datastore export](/bigquery/docs/loading-data-cloud-datastore)
        *   [Load data from a Firestore export](/bigquery/docs/loading-data-cloud-firestore)
        *   [Load data using the Storage Write API](/bigquery/docs/write-api-batch-load)
        *   [Load data into partitioned tables](/bigquery/docs/load-data-partitioned-tables)
        
    *   Write and read data with the Storage API
        
        *   [Read data with the Storage Read API](/bigquery/docs/reference/storage)
        *   Write data with the Storage Write API
            
            *   [Introduction](/bigquery/docs/write-api)
            *   [Stream data with the Storage Write API](/bigquery/docs/write-api-streaming)
            *   [Batch load data with the Storage Write API](/bigquery/docs/write-api-batch)
            *   [Best practices](/bigquery/docs/write-api-best-practices)
            *   [Supported protocol buffer and Arrow data types](/bigquery/docs/supported-data-types)
            *   [Stream updates with change data capture](/bigquery/docs/change-data-capture)
            *   [Use the legacy streaming API](/bigquery/docs/streaming-data-into-bigquery)
            
        
    *   [Load data from other Google services](/bigquery/docs/load-data-google-services)
    *   [Discover and catalog Cloud Storage data](/bigquery/docs/automatic-discovery)
    *   [Load data using third-party apps](/bigquery/docs/load-data-third-party)
    *   [Load data using cross-cloud operations](/bigquery/docs/load-data-using-cross-cloud-transfer)
    
*   Transform data
    
    *   [Introduction](/bigquery/docs/transform-intro)
    *   Prepare data
        
        *   [Introduction](/bigquery/docs/data-prep-introduction)
        *   [Prepare data with Gemini](/bigquery/docs/data-prep-get-suggestions)
        
    *   [Transform with DML](/bigquery/docs/data-manipulation-language)
    *   [Transform data in partitioned tables](/bigquery/docs/using-dml-with-partitioned-tables)
    *   [Work with change history](/bigquery/docs/change-history)
    *   Transform data with pipelines
        
        *   [Introduction](/bigquery/docs/pipelines-introduction)
        *   [Create pipelines](/bigquery/docs/create-pipelines)
        
    
*   Export data
    
    *   [Introduction](/bigquery/docs/export-intro)
    *   [Export query results](/bigquery/docs/export-file)
    *   [Export to Cloud Storage](/bigquery/docs/exporting-data)
    *   [Export to Bigtable](/bigquery/docs/export-to-bigtable)
    *   [Export to Spanner](/bigquery/docs/export-to-spanner)
    *   [Export to Pub/Sub](/bigquery/docs/export-to-pubsub)
    *   [Export as Protobuf columns](/bigquery/docs/protobuf-export)
    
*   Analyze
    
*   [Introduction](/bigquery/docs/query-overview)
*   [Search for resources](/bigquery/docs/search-resources)
*   Explore your data
    
    *   [Create queries with table explorer](/bigquery/docs/table-explorer)
    *   [Profile your data](/bigquery/docs/data-profile-scan)
    *   [Generate data insights](/bigquery/docs/data-insights)
    *   [Analyze with a data canvas](/bigquery/docs/data-canvas)
    *   [Analyze data with Gemini](/bigquery/docs/gemini-analyze-data)
    
*   Query BigQuery data
    
    *   [Run a query](/bigquery/docs/running-queries)
    *   [Write queries with Gemini](/bigquery/docs/write-sql-gemini)
    *   [Write query results](/bigquery/docs/writing-results)
    *   Query data with SQL
        
        *   [Introduction](/bigquery/docs/introduction-sql)
        *   [Arrays](/bigquery/docs/arrays)
        *   [JSON data](/bigquery/docs/json-data)
        *   [Multi-statement queries](/bigquery/docs/multi-statement-queries)
        *   [Parameterized queries](/bigquery/docs/parameterized-queries)
        *   [Pipe syntax](/bigquery/docs/pipe-syntax-guide)
        *   [Analyze data using pipe syntax](/bigquery/docs/analyze-data-pipe-syntax)
        *   [Recursive CTEs](/bigquery/docs/recursive-ctes)
        *   [Sketches](/bigquery/docs/sketches)
        *   [Table sampling](/bigquery/docs/table-sampling)
        *   [Time series](/bigquery/docs/working-with-time-series)
        *   [Transactions](/bigquery/docs/transactions)
        *   [Wildcard tables](/bigquery/docs/querying-wildcard-tables)
        
    *   Use geospatial analytics
        
        *   [Introduction](/bigquery/docs/geospatial-intro)
        *   [Work with geospatial analytics](/bigquery/docs/geospatial-data)
        *   [Work with raster data](/bigquery/docs/raster-data)
        *   [Best practices for spatial analysis](/bigquery/docs/best-practices-spatial-analysis)
        *   [Visualize geospatial data](/bigquery/docs/geospatial-visualize)
        *   [Grid systems for spatial analysis](/bigquery/docs/grid-systems-spatial-analysis)
        *   [Geospatial analytics syntax reference](/bigquery/docs/reference/standard-sql/geography_functions)
        *   Geospatial analytics tutorials
            
            *   [Get started with geospatial analytics](/bigquery/docs/geospatial-get-started)
            *   [Use geospatial analytics to plot a hurricane's path](/bigquery/docs/geospatial-tutorial-hurricane)
            *   [Visualize geospatial analytics data in a Colab notebook](/bigquery/docs/geospatial-visualize-colab)
            *   [Use raster data to analyze temperature](/bigquery/docs/raster-tutorial-weather)
            
        
    *   Search data
        
        *   [Search indexed data](/bigquery/docs/search)
        *   [Work with text analyzers](/bigquery/docs/text-analysis-search)
        
    *   [Access historical data](/bigquery/docs/access-historical-data)
    
*   Work with queries
    
    *   Save queries
        
        *   [Introduction](/bigquery/docs/saved-queries-introduction)
        *   [Create saved queries](/bigquery/docs/work-with-saved-queries)
        
    *   Continuous queries
        
        *   [Introduction](/bigquery/docs/continuous-queries-introduction)
        *   [Create continuous queries](/bigquery/docs/continuous-queries)
        
    *   [Use cached results](/bigquery/docs/cached-results)
    *   Use sessions
        
        *   [Introduction](/bigquery/docs/sessions-intro)
        *   [Work with sessions](/bigquery/docs/sessions)
        *   [Write queries in sessions](/bigquery/docs/sessions-write-queries)
        
    *   [Troubleshoot queries](/bigquery/docs/troubleshoot-queries)
    *   Optimize queries
        
        *   [Introduction](/bigquery/docs/best-practices-performance-overview)
        *   [Use the query plan explanation](/bigquery/docs/query-plan-explanation)
        *   [Get query performance insights](/bigquery/docs/query-insights)
        *   [Optimize query computation](/bigquery/docs/best-practices-performance-compute)
        *   [Use history-based optimizations](/bigquery/docs/history-based-optimizations)
        *   [Optimize storage for query performance](/bigquery/docs/best-practices-storage)
        *   [Use materialized views](/bigquery/docs/materialized-views-use)
        *   [Use BI Engine](/bigquery/docs/bi-engine-query)
        *   [Use nested and repeated data](/bigquery/docs/best-practices-performance-nested)
        *   [Optimize functions](/bigquery/docs/best-practices-performance-functions)
        *   [Use the advanced runtime](/bigquery/docs/advanced-runtime)
        *   [Use primary and foreign keys](/bigquery/docs/primary-foreign-keys)
        
    
*   Analyze multimodal data
    
    *   [Introduction](/bigquery/docs/analyze-multimodal-data)
    *   [Analyze multimodal data with SQL and Python UDFs](/bigquery/docs/multimodal-data-sql-tutorial)
    *   [Analyze multimodal data with BigQuery DataFrames](/bigquery/docs/multimodal-data-dataframes-tutorial)
    
*   Query external data sources
    
    *   Manage open source metadata with BigLake metastore
        
        *   [Introduction](/bigquery/docs/about-blms)
        *   [Use with tables in BigQuery](/bigquery/docs/blms-use-tables)
        *   [Use with Spark in BigQuery notebooks](/bigquery/docs/use-spark)
        *   [Use with Dataproc](/bigquery/docs/blms-use-dataproc)
        *   [Use with Dataproc Serverless](/bigquery/docs/blms-use-dataproc-serverless)
        *   [Use with Spark stored procedures](/bigquery/docs/blms-use-stored-procedures)
        *   [Manage Iceberg resources](/bigquery/docs/blms-manage-resources)
        *   [Create and query tables from Spark](/bigquery/docs/blms-query-tables)
        *   [Customize with additional features](/bigquery/docs/blms-features)
        *   [Use with the Iceberg REST catalog](/bigquery/docs/blms-rest-catalog)
        *   [Migrate from Dataproc Metastore](/bigquery/docs/blms-dpms-migration-tool)
        
    *   [Optimal data and metadata formats for lakehouses](/bigquery/docs/lakehouse-recommendations)
    *   Use external tables and datasets
        
        *   Amazon S3 data
            
            *   [Query Amazon S3 data](/bigquery/docs/query-aws-data)
            *   [Export query results to Amazon S3](/bigquery/docs/omni-aws-export-results-to-s3)
            
        *   [Query Apache Iceberg data](/bigquery/docs/query-iceberg-data)
        *   [Query open table formats with manifests](/bigquery/docs/query-open-table-format-using-manifest-files)
        *   Azure Blob Storage data
            
            *   [Query Azure Blob Storage data](/bigquery/docs/query-azure-data)
            *   [Export query results to Azure Blob Storage](/bigquery/docs/omni-azure-export-results-to-azure-storage)
            
        *   [Query Cloud Bigtable data](/bigquery/docs/external-data-bigtable)
        *   Cloud Storage data
            
            *   [Query Cloud Storage data in BigLake tables](/bigquery/docs/query-cloud-storage-using-biglake)
            *   [Query Cloud Storage data in external tables](/bigquery/docs/query-cloud-storage-data)
            
        *   [Work with Salesforce Data Cloud data](/bigquery/docs/salesforce-quickstart)
        *   [Query Google Drive data](/bigquery/docs/query-drive-data)
        *   [Create AWS Glue federated datasets](/bigquery/docs/glue-federated-datasets)
        *   [Create Spanner external datasets](/bigquery/docs/spanner-external-datasets)
        
    *   Run federated queries
        
        *   [Federated queries](/bigquery/docs/federated-queries-intro)
        *   [Query SAP Datasphere data](/bigquery/docs/sap-datasphere-federated-queries)
        *   [Query AlloyDB data](/bigquery/docs/alloydb-federated-queries)
        *   [Query Spanner data](/bigquery/docs/spanner-federated-queries)
        *   [Query Cloud SQL data](/bigquery/docs/cloud-sql-federated-queries)
        
    
*   Use notebooks
    
    *   [Introduction](/bigquery/docs/programmatic-analysis)
    *   Use Colab notebooks
        
        *   [Introduction](/bigquery/docs/notebooks-introduction)
        *   [Create notebooks](/bigquery/docs/create-notebooks)
        *   [Explore query results](/bigquery/docs/explore-data-colab)
        *   [Use Spark](/bigquery/docs/use-spark)
        *   [Use Colab Data Science Agent](/bigquery/docs/colab-data-science-agent)
        
    *   Use DataFrames
        
        *   [Introduction](/bigquery/docs/bigquery-dataframes-introduction)
        *   [Use DataFrames](/bigquery/docs/use-bigquery-dataframes)
        *   [Use the data type system](/bigquery/docs/dataframes-data-types)
        *   [Manage sessions and I/O](/bigquery/docs/dataframes-sessions-io)
        *   [Visualize graphs](/bigquery/docs/dataframes-visualizations)
        *   [Use DataFrames in dbt](/bigquery/docs/dataframes-dbt)
        
    *   Use Jupyter notebooks
        
        *   [Use the BigQuery JupyterLab plugin](/bigquery/docs/jupyterlab-plugin)
        
    
*   Use analysis and BI tools
    
    *   [Introduction](/bigquery/docs/data-analysis-tools-intro)
    *   [Use Connected Sheets](/bigquery/docs/connected-sheets)
    *   [Use Tableau Desktop](/bigquery/docs/analyze-data-tableau)
    *   [Use Looker](/bigquery/docs/looker)
    *   [Use Looker Studio](/bigquery/docs/visualize-looker-studio)
    *   [Use third-party tools](/bigquery/docs/third-party-integration)
    *   Google Cloud Ready - BigQuery
        
        *   [Overview](/bigquery/docs/bigquery-ready-overview)
        *   [Partners](/bigquery/docs/bigquery-ready-partners)
        
    
*   AI and machine learning
    
*   [Introduction](/bigquery/docs/bqml-introduction)
*   Generative AI and pretrained models
    
    *   Choose generative AI and task-specific functions
        
        *   [Choose a natural language processing function](/bigquery/docs/choose-ml-text-function)
        *   [Choose a document processing function](/bigquery/docs/choose-document-processing-function)
        *   [Choose a transcription function](/bigquery/docs/choose-transcription-function)
        
    *   Generative AI
        
        *   [Overview](/bigquery/docs/generative-ai-overview)
        *   Built-in models
            
            *   [The TimesFM time series forecasting model](/bigquery/docs/timesfm-model)
            
        *   Tutorials
            
            *   Generate text
                
                *   [Generate text using public data and Gemini](/bigquery/docs/generate-text-tutorial-gemini)
                *   [Generate text using public data and Gemma](/bigquery/docs/generate-text-tutorial-gemma)
                *   [Generate text using your data](/bigquery/docs/generate-text)
                *   [Handle quota errors by calling ML.GENERATE\_TEXT iteratively](/bigquery/docs/iterate-generate-text-calls)
                *   [Analyze images with a Gemini vision model](/bigquery/docs/image-analysis)
                *   Tune text generation models
                    
                    *   [Tune a model using your data](/bigquery/docs/generate-text-tuning)
                    *   [Use tuning and evaluation to improve model performance](/bigquery/docs/tune-evaluate)
                    
                
            *   Generate structured data
                
                *   [Generate structured data](/bigquery/docs/generate-table)
                
            *   Generate embeddings
                
                *   [Generate text embeddings using an LLM](/bigquery/docs/generate-text-embedding)
                *   [Generate image embeddings using an LLM](/bigquery/docs/generate-visual-content-embedding)
                *   [Generate video embeddings using an LLM](/bigquery/docs/generate-video-embedding)
                *   [Handle quota errors by calling ML.GENERATE\_EMBEDDING iteratively](/bigquery/docs/iterate-generate-embedding-calls)
                *   [Generate and search multimodal embeddings](/bigquery/docs/generate-multimodal-embeddings)
                *   [Generate text embeddings using pretrained TensorFlow models](/bigquery/docs/generate-embedding-with-tensorflow-models)
                
            *   Vector search
                
                *   [Search embeddings with vector search](/bigquery/docs/vector-search)
                *   [Perform semantic search and retrieval-augmented generation](/bigquery/docs/vector-index-text-search-tutorial)
                
            
        
    *   Task-specific solutions
        
        *   [Overview](/bigquery/docs/ai-application-overview)
        *   Tutorials
            
            *   Natural language processing
                
                *   [Understand text](/bigquery/docs/understand-text)
                *   [Translate text](/bigquery/docs/translate-text)
                
            *   Document processing
                
                *   [Process documents](/bigquery/docs/process-document)
                *   [Parse PDFs in a retrieval-augmented generation pipeline](/bigquery/docs/rag-pipeline-pdf)
                
            *   Speech recognition
                
                *   [Transcribe audio files](/bigquery/docs/transcribe)
                
            *   Computer vision
                
                *   [Annotate images](/bigquery/docs/annotate-image)
                *   [Run inference on image data](/bigquery/docs/object-table-inference)
                *   [Analyze images with an imported classification model](/bigquery/docs/inference-tutorial-resnet)
                *   [Analyze images with an imported feature vector model](/bigquery/docs/inference-tutorial-mobilenet)
                
            
        
    
*   Machine learning
    
    *   ML models and MLOps
        
        *   [End-to-end journey per model](/bigquery/docs/e2e-journey)
        *   [Model creation](/bigquery/docs/model-overview)
        *   [Hyperparameter tuning overview](/bigquery/docs/hp-tuning-overview)
        *   [Model evaluation overview](/bigquery/docs/evaluate-overview)
        *   [Model inference overview](/bigquery/docs/inference-overview)
        *   [Explainable AI overview](/bigquery/docs/xai-overview)
        *   [Model weights overview](/bigquery/docs/weights-overview)
        *   [ML pipelines overview](/bigquery/docs/ml-pipelines-overview)
        *   [Model monitoring overview](/bigquery/docs/model-monitoring-overview)
        *   [Manage BigQueryML models in Vertex AI](/bigquery/docs/managing-models-vertex)
        
    *   Use cases
        
        *   [Forecasting](/bigquery/docs/forecasting-overview)
        *   [Anomaly detection](/bigquery/docs/anomaly-detection-overview)
        *   [Recommendation](/bigquery/docs/recommendation-overview)
        *   [Classification](/bigquery/docs/classification-overview)
        *   [Regression](/bigquery/docs/regression-overview)
        *   [Dimensionality reduction](/bigquery/docs/dimensionality-reduction-overview)
        *   [Clustering](/bigquery/docs/clustering-overview)
        
    *   Tutorials
        
        *   [Get started with BigQuery ML using SQL](/bigquery/docs/create-machine-learning-model)
        *   [Get started with BigQuery ML using the Cloud console](/bigquery/docs/create-machine-learning-model-console)
        *   Regression and classification
            
            *   [Create a linear regression model](/bigquery/docs/linear-regression-tutorial)
            *   [Create a logistic regression classification model](/bigquery/docs/logistic-regression-prediction)
            *   [Create a boosted tree classification model](/bigquery/docs/boosted-tree-classifier-tutorial)
            
        *   Clustering
            
            *   [Cluster data with a k-means model](/bigquery/docs/kmeans-tutorial)
            
        *   Recommendation
            
            *   [Create recommendations based on explicit feedback with a matrix factorization model](/bigquery/docs/bigqueryml-mf-explicit-tutorial)
            *   [Create recommendations based on implicit feedback with a matrix factorization model](/bigquery/docs/bigqueryml-mf-implicit-tutorial)
            
        *   Time series forecasting
            
            *   [Forecast a single time series with an ARIMA\_PLUS univariate model](/bigquery/docs/arima-single-time-series-forecasting-tutorial)
            *   [Forecast multiple time series with an ARIMA\_PLUS univariate model](/bigquery/docs/arima-multiple-time-series-forecasting-tutorial)
            *   [Forecast time series with a TimesFM univariate model](/bigquery/docs/timesfm-time-series-forecasting-tutorial)
            *   [Scale an ARIMA\_PLUS univariate model to millions of time series](/bigquery/docs/arima-speed-up-tutorial)
            *   [Forecast a single time series with a multivariate model](/bigquery/docs/arima-plus-xreg-single-time-series-forecasting-tutorial)
            *   [Forecast multiple time series with a multivariate model](/bigquery/docs/arima-plus-xreg-multiple-time-series-forecasting-tutorial)
            *   [Use custom holidays with an ARIMA\_PLUS univariate model](/bigquery/docs/time-series-forecasting-holidays-tutorial)
            *   [Limit forecasted values for an ARIMA\_PLUS univariate model](/bigquery/docs/arima-time-series-forecasting-with-limits-tutorial)
            *   [Forecast hierarchical time series with an ARIMA\_PLUS univariate model](/bigquery/docs/arima-time-series-forecasting-with-hierarchical-time-series)
            
        *   Anomaly detection
            
            *   [Anomaly detection with a multivariate time series](/bigquery/docs/time-series-anomaly-detection-tutorial)
            
        *   Imported and remote models
            
            *   [Make predictions with imported TensorFlow models](/bigquery/docs/making-predictions-with-imported-tensorflow-models)
            *   [Make predictions with scikit-learn models in ONNX format](/bigquery/docs/making-predictions-with-sklearn-models-in-onnx-format)
            *   [Make predictions with PyTorch models in ONNX format](/bigquery/docs/making-predictions-with-pytorch-models-in-onnx-format)
            *   [Make predictions with remote models on Vertex AI](/bigquery/docs/bigquery-ml-remote-model-tutorial)
            
        *   Hyperparameter tuning
            
            *   [Improve model performance with hyperparameter tuning](/bigquery/docs/hyperparameter-tuning-tutorial)
            
        *   Export models
            
            *   [Export a BigQuery ML model for online prediction](/bigquery/docs/export-model-tutorial)
            
        
    
*   Augmented analytics
    
    *   [Contribution analysis](/bigquery/docs/contribution-analysis)
    *   Tutorials
        
        *   [Get data insights from contribution analysis using a summable metric](/bigquery/docs/get-contribution-analysis-insights)
        *   [Get data insights from contribution analysis using a summable ratio metric](/bigquery/docs/get-contribution-analysis-insights-sum-ratio)
        
    
*   Create and manage features
    
    *   [Feature preprocessing overview](/bigquery/docs/preprocess-overview)
    *   [Supported input feature types](/bigquery/docs/input-feature-types)
    *   [Automatic preprocessing](/bigquery/docs/auto-preprocessing)
    *   [Manual preprocessing](/bigquery/docs/manual-preprocessing)
    *   [Feature serving](/bigquery/docs/feature-serving)
    *   [Perform feature engineering with the TRANSFORM clause](/bigquery/docs/bigqueryml-transform)
    
*   Work with models
    
    *   [List models](/bigquery/docs/listing-models)
    *   [Manage models](/bigquery/docs/managing-models)
    *   [Get model metadata](/bigquery/docs/getting-model-metadata)
    *   [Update model metadata](/bigquery/docs/updating-model-metadata)
    *   [Export models](/bigquery/docs/exporting-models)
    *   [Delete models](/bigquery/docs/deleting-models)
    
*   [Reference patterns](/bigquery/docs/reference-patterns)
*   Administer
    
*   [Introduction](/bigquery/docs/admin-intro)
*   Manage resources
    
    *   [Organize resources](/bigquery/docs/resource-hierarchy)
    *   [Understand reliability](/bigquery/docs/reliability-intro)
    *   Manage code assets
        
        *   [Manage data preparations](/bigquery/docs/manage-data-preparations)
        *   [Manage notebooks](/bigquery/docs/manage-notebooks)
        *   [Manage saved queries](/bigquery/docs/manage-saved-queries)
        *   [Manage pipelines](/bigquery/docs/manage-pipelines)
        
    *   Manage tables
        
        *   [Manage tables](/bigquery/docs/managing-tables)
        *   [Manage table data](/bigquery/docs/managing-table-data)
        *   [Modify table schemas](/bigquery/docs/managing-table-schemas)
        *   [Restore deleted tables](/bigquery/docs/restore-deleted-tables)
        
    *   Manage table clones
        
        *   [Introduction](/bigquery/docs/table-clones-intro)
        *   [Create table clones](/bigquery/docs/table-clones-create)
        
    *   Manage table snapshots
        
        *   [Introduction](/bigquery/docs/table-snapshots-intro)
        *   [Create table snapshots](/bigquery/docs/table-snapshots-create)
        *   [Restore table snapshots](/bigquery/docs/table-snapshots-restore)
        *   [List table snapshots](/bigquery/docs/table-snapshots-list)
        *   [View table snapshot metadata](/bigquery/docs/table-snapshots-metadata)
        *   [Update table snapshot metadata](/bigquery/docs/table-snapshots-update)
        *   [Delete table snapshots](/bigquery/docs/table-snapshots-delete)
        *   [Create periodic table snapshots](/bigquery/docs/table-snapshots-scheduled)
        
    *   [Manage configuration settings](/bigquery/docs/default-configuration)
    *   Manage datasets
        
        *   [Manage datasets](/bigquery/docs/managing-datasets)
        *   [Update dataset properties](/bigquery/docs/updating-datasets)
        *   [Restore deleted datasets](/bigquery/docs/restore-deleted-datasets)
        
    *   [Manage materialized views](/bigquery/docs/materialized-views-manage)
    *   [Manage materialized view replicas](/bigquery/docs/materialized-view-replicas-manage)
    
*   Schedule resources
    
    *   [Introduction](/bigquery/docs/orchestrate-workloads)
    *   Schedule code assets
        
        *   [Schedule data preparations](/bigquery/docs/orchestrate-data-preparations)
        *   [Schedule notebooks](/bigquery/docs/orchestrate-notebooks)
        *   [Schedule pipelines](/bigquery/docs/schedule-pipelines)
        *   [Schedule DAGs](/bigquery/docs/orchestrate-dags)
        
    *   Schedule jobs and queries
        
        *   [Run jobs programmatically](/bigquery/docs/running-jobs)
        *   [Schedule queries](/bigquery/docs/scheduling-queries)
        
    
*   Workload management
    
    *   [Introduction](/bigquery/docs/reservations-intro)
    *   [Slots](/bigquery/docs/slots)
    *   [Slot reservations](/bigquery/docs/reservations-workload-management)
    *   [Slots autoscaling](/bigquery/docs/slots-autoscaling-intro)
    *   Use reservations
        
        *   [Get started](/bigquery/docs/reservations-get-started)
        *   [Estimate slot capacity requirements](/bigquery/docs/slot-estimator)
        *   [View slot recommendations and insights](/bigquery/docs/slot-recommender)
        *   [Purchase and manage slot commitments](/bigquery/docs/reservations-commitments)
        *   [Work with slot reservations](/bigquery/docs/reservations-tasks)
        *   [Work with reservation assignments](/bigquery/docs/reservations-assignments)
        
    *   [Manage jobs](/bigquery/docs/managing-jobs)
    *   [Use query queues](/bigquery/docs/query-queues)
    *   Legacy reservations
        
        *   [Introduction to legacy reservations](/bigquery/docs/reservations-intro-legacy)
        *   [Legacy slot commitments](/bigquery/docs/reservations-details-legacy)
        *   [Purchase and manage legacy slot commitments](/bigquery/docs/reservations-commitments-legacy)
        *   [Work with legacy slot reservations](/bigquery/docs/reservations-tasks-legacy)
        
    *   Manage BI Engine
        
        *   [Introduction](/bigquery/docs/bi-engine-intro)
        *   [Reserve BI Engine capacity](/bigquery/docs/bi-engine-reserve-capacity)
        
    
*   Monitor workloads
    
    *   [Introduction](/bigquery/docs/monitoring)
    *   [Monitor resource utilization](/bigquery/docs/admin-resource-charts)
    *   [Monitor jobs](/bigquery/docs/admin-jobs-explorer)
    *   [Monitor sharing listings](/bigquery/docs/analytics-hub-monitor-listings)
    *   [Monitor BI Engine](/bigquery/docs/bi-engine-monitor)
    *   [Monitor Data Transfer Service](/bigquery/docs/dts-monitor)
    *   [Monitor materialized views](/bigquery/docs/materialized-views-monitor)
    *   [Monitor reservations](/bigquery/docs/reservations-monitoring)
    *   [Monitor continuous queries](/bigquery/docs/continuous-queries-monitor)
    *   [Dashboards, charts, and alerts](/bigquery/docs/monitoring-dashboard)
    *   [Set up alerts with scheduled queries](/bigquery/docs/create-alert-scheduled-query)
    
*   Optimize resources
    
    *   Control costs
        
        *   [Estimate and control costs](/bigquery/docs/best-practices-costs)
        *   [Create custom query quotas](/bigquery/docs/custom-quotas)
        
    *   Optimize with recommendations
        
        *   [Introduction](/bigquery/docs/recommendations-intro)
        *   [Manage cluster and partition recommendations](/bigquery/docs/manage-partition-cluster-recommendations)
        *   [Manage materialized view recommendations](/bigquery/docs/manage-materialized-recommendations)
        
    *   Organize with labels
        
        *   [Introduction](/bigquery/docs/labels-intro)
        *   [Add labels](/bigquery/docs/adding-labels)
        *   [View labels](/bigquery/docs/viewing-labels)
        *   [Update labels](/bigquery/docs/updating-labels)
        *   [Filter using labels](/bigquery/docs/filtering-labels)
        *   [Delete labels](/bigquery/docs/deleting-labels)
        
    
*   Govern
    
*   [Introduction](/bigquery/docs/data-governance)
*   Manage data quality
    
    *   [Scan for data quality issues](/bigquery/docs/data-quality-scan)
    *   [Data Catalog overview](/bigquery/docs/data-catalog-overview)
    *   [Work with Data Catalog](/bigquery/docs/data-catalog)
    
*   Control access to resources
    
    *   [Introduction](/bigquery/docs/access-control-intro)
    *   [IAM roles and permissions](/bigquery/docs/access-control)
    *   [Changes to dataset-level access controls](/bigquery/docs/dataset-access-control)
    *   [Basic roles and permissions](/bigquery/docs/access-control-basic-roles)
    *   Control access with IAM
        
        *   [Control access to resources with IAM](/bigquery/docs/control-access-to-resources-iam)
        *   [Control access with tags](/bigquery/docs/tags)
        *   [Control access with conditions](/bigquery/docs/conditions)
        *   [Control access with custom constraints](/bigquery/docs/custom-constraints)
        
    *   Control access with authorization
        
        *   [Authorized datasets](/bigquery/docs/authorized-datasets)
        *   [Authorized routines](/bigquery/docs/authorized-routines)
        *   [Authorized views](/bigquery/docs/authorized-views)
        *   Tutorials
            
            *   [Create an authorized view](/bigquery/docs/create-authorized-views)
            
        
    *   Restrict network access
        
        *   [Control access with VPC service controls](/bigquery/docs/vpc-sc)
        *   [Regional endpoints](/bigquery/docs/regional-endpoints)
        
    *   Control column and row access
        
        *   Control access to table columns
            
            *   [Introduction to column-level access control](/bigquery/docs/column-level-security-intro)
            *   [Restrict access with column-level access control](/bigquery/docs/column-level-security)
            *   [Impact on writes](/bigquery/docs/column-level-security-writes)
            
        *   Control access to table rows
            
            *   [Introduction to row-level security](/bigquery/docs/row-level-security-intro)
            *   [Work with row-level security](/bigquery/docs/managing-row-level-security)
            *   [Use row-level security with other BigQuery features](/bigquery/docs/using-row-level-security-with-features)
            *   [Best practices for row-level security](/bigquery/docs/best-practices-row-level-security)
            
        *   Manage policy tags
            
            *   [Manage policy tags across locations](/bigquery/docs/managing-policy-tags-across-locations)
            *   [Best practices for using policy tags](/bigquery/docs/best-practices-policy-tags)
            
        
    *   Protect sensitive data
        
        *   Mask data in table columns
            
            *   [Introduction to data masking](/bigquery/docs/column-data-masking-intro)
            *   [Mask column data](/bigquery/docs/column-data-masking)
            
        *   Anonymize data with differential privacy
            
            *   [Use differential privacy](/bigquery/docs/differential-privacy)
            *   [Extend differential privacy](/bigquery/docs/extend-differential-privacy)
            
        *   [Restrict data access using analysis rules](/bigquery/docs/analysis-rules)
        *   [Use Sensitive Data Protection](/bigquery/docs/scan-with-dlp)
        
    *   Manage encryption
        
        *   [Encryption at rest](/bigquery/docs/encryption-at-rest)
        *   [Customer-managed encryption keys](/bigquery/docs/customer-managed-encryption)
        *   [Column-level encryption with Cloud KMS](/bigquery/docs/column-key-encrypt)
        *   [AEAD encryption](/bigquery/docs/aead-encryption-concepts)
        
    
*   Share data
    
    *   [Introduction](/bigquery/docs/analytics-hub-introduction)
    *   [Manage data exchanges](/bigquery/docs/analytics-hub-manage-exchanges)
    *   [Manage listings](/bigquery/docs/analytics-hub-manage-listings)
    *   [Manage subscriptions](/bigquery/docs/analytics-hub-manage-subscriptions)
    *   [Configure user roles](/bigquery/docs/analytics-hub-grant-roles)
    *   [View and subscribe to listings](/bigquery/docs/analytics-hub-view-subscribe-listings)
    *   [Share sensitive data with data clean rooms](/bigquery/docs/data-clean-rooms)
    *   Entity resolution
        
        *   [Introduction](/bigquery/docs/entity-resolution-intro)
        *   [Use entity resolution](/bigquery/docs/entity-resolution-setup)
        
    *   [VPC Service Controls for Sharing](/bigquery/docs/analytics-hub-vpc-sc-rules)
    *   [Stream sharing with Pub/Sub](/bigquery/docs/analytics-hub-stream-sharing)
    *   [Commercialize listings on Cloud Marketplace](/bigquery/docs/analytics-hub-cloud-marketplace)
    
*   Audit
    
    *   [Introduction](/bigquery/docs/introduction-audit-workloads)
    *   [Audit policy tags](/bigquery/docs/auditing-policy-tags)
    *   [View Data Policy audit logs](/bigquery/docs/column-data-masking-audit-logging)
    *   [Data Transfer Service audit logs](/bigquery/docs/audit-logging)
    *   [Sharing audit logs](/bigquery/docs/analytics-hub-audit-logging)
    *   [BigQuery audit logs reference](/bigquery/docs/reference/auditlogs)
    *   [Migrate audit logs](/bigquery/docs/reference/auditlogs/migration)
    *   [BigLake API audit logs](/bigquery/docs/biglake-audit-logging)
    *   [BigQuery Migration API audit logs](/bigquery/docs/reference/auditlogs/audit-logging-bq-migration)
    
*   Develop
    
*   [Introduction](/bigquery/docs/developer-overview)
*   [BigQuery code samples](/bigquery/docs/samples)
*   BigQuery API basics
    
    *   [BigQuery APIs and libraries overview](/bigquery/docs/reference/libraries-overview)
    *   Authentication
        
        *   [Introduction](/bigquery/docs/authentication)
        *   [Get started](/bigquery/docs/authentication/getting-started)
        *   [Authenticate as an end user](/bigquery/docs/authentication/end-user-installed)
        *   [Authenticate with JSON Web Tokens](/bigquery/docs/json-web-tokens)
        
    *   [Run jobs programmatically](/bigquery/docs/running-jobs)
    *   [Paginate with BigQuery API](/bigquery/docs/paging-results)
    *   [API performance tips](/bigquery/docs/api-performance)
    *   [Batch requests](/bigquery/batch)
    
*   Repositories
    
    *   [Introduction](/bigquery/docs/repository-intro)
    *   [Create repositories](/bigquery/docs/repositories)
    
*   Workspaces
    
    *   [Introduction](/bigquery/docs/workspaces-intro)
    *   [Create and use workspaces](/bigquery/docs/workspaces)
    
*   [Use the VS Code extension](/bigquery/docs/vs-code-extension)
*   [Choose a Python library](/bigquery/docs/python-libraries)
*   [Use ODBC and JDBC drivers](/bigquery/docs/reference/odbc-jdbc-drivers)
*   [Connect your IDE to BigQuery](/bigquery/docs/pre-built-tools-with-mcp-toolbox)

*   [AI and ML](/docs/ai-ml)
*   [Application development](/docs/application-development)
*   [Application hosting](/docs/application-hosting)
*   [Compute](/docs/compute-area)
*   [Data analytics and pipelines](/docs/data)
*   [Databases](/docs/databases)
*   [Distributed, hybrid, and multicloud](/docs/dhm-cloud)
*   [Generative AI](/docs/generative-ai)
*   [Industry solutions](/docs/industry)
*   [Networking](/docs/networking)
*   [Observability and monitoring](/docs/observability)
*   [Security](/docs/security)
*   [Storage](/docs/storage)

*   [Access and resources management](/docs/access-resources)
*   [Costs and usage management](/docs/costs-usage)
*   [Google Cloud SDK, languages, frameworks, and tools](/docs/devtools)
*   [Infrastructure as code](/docs/iac)
*   [Migration](/docs/migration)

*   [Google Cloud Home](/)
*   [Free Trial and Free Tier](/free)
*   [Architecture Center](/architecture)
*   [Blog](https://cloud.google.com/blog)
*   [Contact Sales](/contact)
*   [Google Cloud Developer Center](/developers)
*   [Google Developer Center](https://developers.google.com/)
*   [Google Cloud Marketplace](https://console.cloud.google.com/marketplace)
*   [Google Cloud Marketplace Documentation](/marketplace/docs)
*   [Google Cloud Skills Boost](https://www.cloudskillsboost.google/paths)
*   [Google Cloud Solution Center](/solutions)
*   [Google Cloud Support](/support-hub)
*   [Google Cloud Tech Youtube Channel](https://www.youtube.com/@googlecloudtech)

*   On this page
*   [When to use clustering](#when_to_use_clustering)
*   [Cluster column types and ordering](#cluster_column_types_and_ordering)
    *   [Cluster column types](#cluster_column_types)
    *   [Cluster column ordering](#cluster_column_ordering)
*   [Block pruning](#block-pruning)
*   [Combine clustered and partitioned tables](#combine-clustered-partitioned-tables)
    *   [Example](#example)
*   [Automatic reclustering](#automatic_reclustering)
*   [Limitations](#limitations)
*   [Clustered table quotas and limits](#clustered_table_quotas_and_limits)
*   [Clustered table pricing](#clustered_table_pricing)
*   [Table security](#table_security)
*   [What's next](#whats_next)

*   [Home](https://cloud.google.com/)
*   [BigQuery](https://cloud.google.com/bigquery)
*   [Documentation](https://cloud.google.com/bigquery/docs)
*   [Guides](https://cloud.google.com/bigquery/docs/introduction)

Was this helpful?

Send feedback

*   On this page
*   [When to use clustering](#when_to_use_clustering)
*   [Cluster column types and ordering](#cluster_column_types_and_ordering)
    *   [Cluster column types](#cluster_column_types)
    *   [Cluster column ordering](#cluster_column_ordering)
*   [Block pruning](#block-pruning)
*   [Combine clustered and partitioned tables](#combine-clustered-partitioned-tables)
    *   [Example](#example)
*   [Automatic reclustering](#automatic_reclustering)
*   [Limitations](#limitations)
*   [Clustered table quotas and limits](#clustered_table_quotas_and_limits)
*   [Clustered table pricing](#clustered_table_pricing)
*   [Table security](#table_security)
*   [What's next](#whats_next)

Introduction to clustered tables

bookmark\_borderbookmark Stay organized with collections Save and categorize content based on your preferences.


===================================================================================================================================================

Clustered tables in BigQuery are tables that have a user-defined column sort order using _clustered columns_. Clustered tables can improve query performance and reduce query costs.

In BigQuery, a _clustered column_ is a user-defined table property that sorts [storage blocks](/bigquery/docs/storage_overview#storage_layout) based on the values in the clustered columns. The storage blocks are adaptively sized based on the size of the table. Colocation occurs at the level of the storage blocks, and not at the level of individual rows; for more information on colocation in this context, see [Clustering](/bigquery/docs/migration/schema-data-overview#clustering).

A clustered table maintains the sort properties in the context of each operation that modifies it. Queries that filter or aggregate by the clustered columns only scan the relevant blocks based on the clustered columns, instead of the entire table or table partition. As a result, BigQuery might not be able to accurately estimate the bytes to be processed by the query or the query costs, but it attempts to reduce the total bytes at execution.

When you cluster a table using multiple columns, the column order determines which columns take precedence when BigQuery sorts and groups the data into storage blocks, as seen in the following example. Table 1 shows the logical storage block layout of an unclustered table. In comparison, table 2 is only clustered by the `Country` column, whereas table 3 is clustered by multiple columns, `Country` and `Status`.

![BigQuery sorts data in clustered tables to improve query performance.](/static/bigquery/images/clustering-tables.png)

When you query a clustered table, you don't receive an accurate query cost estimate before query execution because the number of storage blocks to be scanned is not known before query execution. The final cost is determined after query execution is complete and is based on the specific storage blocks that were scanned.

When to use clustering
----------------------

Clustering addresses how a table is stored so it's generally a good first option for improving query performance. You should therefore always consider clustering given the following advantages it provides:

*   Unpartitioned tables larger than 64 MB are likely to benefit from clustering. Similarly, table partitions larger than 64 MB are also likely to benefit from clustering. Clustering smaller tables or partitions is possible, but the performance improvement is usually negligible.
*   If your queries commonly filter on particular columns, clustering accelerates queries because the query only scans the blocks that match the filter.
*   If your queries filter on columns that have many distinct values (high cardinality), clustering accelerates these queries by providing BigQuery with detailed metadata for where to get input data.
*   Clustering enables your table's underlying storage blocks to be adaptively sized based on the size of the table.

You might consider [partitioning](/bigquery/docs/partitioned-tables) your table in addition to clustering. In this approach, you first segment data into partitions, and then you cluster the data within each partition by the clustering columns. Consider this approach in the following circumstances:

*   You need a strict query cost estimate before you run a query. The cost of queries over clustered tables can only be determined after the query is run. Partitioning provides granular query cost estimates before you run a query.
*   Partitioning your table results in an average partition size of at least 10 GB per partition. Creating many small partitions increases the table's metadata, and can affect metadata access times when querying the table.
*   You need to continually update your table but still want to [take advantage of long-term storage pricing](/bigquery/docs/best-practices-storage#store-data-bigquery). Partitioning enables each partition to be considered separately for eligibility for long term pricing. If your table is not partitioned, then your entire table must not be edited for 90 consecutive days to be considered for long term pricing.

For more information, see [Combine clustered and partitioned tables](#combine-clustered-partitioned-tables).

Cluster column types and ordering
---------------------------------

This section describes column types and how column order works in table clustering.

### Cluster column types

Cluster columns must be top-level, non-repeated columns that are one of the following types:

*   `BIGNUMERIC`
*   `BOOL`
*   `DATE`
*   `DATETIME`
*   `GEOGRAPHY`
*   `INT64`
*   `NUMERIC`
*   `RANGE`
*   `STRING`
*   `TIMESTAMP`

For more information about data types, see [GoogleSQL data types](/bigquery/docs/reference/standard-sql/data-types).

### Cluster column ordering

The order of clustered columns affects query performance. In the following example, the `Orders` table is clustered using a column sort order of `Order_Date`, `Country`, and `Status`. The first clustered column in this example is `Order_Date`, so a query that filters on `Order_Date` and `Country` is optimized for clustering, whereas a query that filters on only `Country` and `Status` is not optimized.

![Queries on clustered tables must include clustered columns in order starting from the first.](/static/bigquery/images/optimize-query-clustering-tables.png)

Block pruning
-------------

Clustered tables can help you to reduce query costs by pruning data so it's not processed by the query. This process is called block pruning. BigQuery sorts the data in a clustered table based on the values in the clustering columns and organizes them into blocks.

When you run a query against a clustered table, and the query includes a filter on the clustered columns, BigQuery uses the filter expression and the block metadata to prune the blocks scanned by the query. This allows BigQuery to scan only the relevant blocks.

When a block is pruned, it is not scanned. Only the scanned blocks are used to calculate the bytes of data processed by the query. The number of bytes processed by a query against a clustered table equals the sum of the bytes read in each column referenced by the query in the scanned blocks.

If a clustered table is referenced multiple times in a query that uses several filters, BigQuery charges for scanning the columns in the appropriate blocks in each of the respective filters. For an example of how block pruning works, see [Example](#example).

Combine clustered and partitioned tables
----------------------------------------

You can combine table clustering with [table partitioning](/bigquery/docs/partitioned-tables) to achieve finely-grained sorting for further query optimization.

In a partitioned table, data is stored in physical blocks, each of which holds one partition of data. Each partitioned table maintains various metadata about the sort properties across all operations that modify it. The metadata lets BigQuery more accurately estimate a query cost before the query is run. However, partitioning requires BigQuery to maintain more metadata than with an unpartitioned table. As the number of partitions increases, the amount of metadata to maintain increases.

When you create a table that is clustered and partitioned, you can achieve more finely grained sorting, as the following diagram shows:

![Comparing tables that are not clustered or partitioned to tables that are clustered and partitioned.](/static/bigquery/images/clustering-and-partitioning-tables.png)

### Example

You have a clustered table named `ClusteredSalesData`. The table is partitioned by the `timestamp` column, and it is clustered by the `customer_id` column. The data is organized into the following set of blocks:

Partition identifier

Block ID

Minimum value for customer\_id in the block

Maximum value for customer\_id in the block

20160501

B1

10000

19999

20160501

B2

20000

24999

20160502

B3

15000

17999

20160501

B4

22000

27999

You run the following query against the table. The query contains a filter on the `customer_id` column.

SELECT
  SUM(totalSale)
FROM
  \`mydataset.ClusteredSalesData\`
WHERE
  customer\_id BETWEEN 20000
  AND 23000
  AND DATE(timestamp) \= "2016-05-01"

The preceding query involves the following steps:

*   Scans the `timestamp`, `customer_id`, and `totalSale` columns in blocks B2 and B4.
*   Prunes the B3 block because of the `DATE(timestamp) = "2016-05-01"` filter predicate on the `timestamp` partitioning column.
*   Prunes the B1 block because of the `customer_id BETWEEN 20000 AND 23000` filter predicate on the `customer_id` clustering column.

Automatic reclustering
----------------------

As data is added to a clustered table, the new data is organized into blocks, which might create new storage blocks or update existing blocks. Block optimization is required for optimal query and storage performance because new data might not be grouped with existing data that has the same cluster values.

To maintain the performance characteristics of a clustered table, BigQuery performs automatic reclustering in the background. For partitioned tables, clustering is maintained for data within the scope of each partition.

**Note:** Automatic reclustering has no effect on query capacity.

Limitations
-----------

*   Only GoogleSQL is supported for querying clustered tables and for writing query results to clustered tables.
*   You can only specify up to four clustering columns. If you need additional columns, consider combining clustering with partitioning.
*   When using `STRING` type columns for clustering, BigQuery uses only the first 1,024 characters to cluster the data. The values in the columns can themselves be longer than 1,024 characters.
*   If you alter an existing non-clustered table to be clustered, the existing data is not automatically clustered. Only new data that's stored using the clustered columns is subject to automatic reclustering. For more information about reclustering existing data using an [`UPDATE` statement](/bigquery/docs/reference/standard-sql/dml-syntax#update_statement), see [Modify clustering specification](/bigquery/docs/creating-clustered-tables#modifying-cluster-spec).

Clustered table quotas and limits
---------------------------------

BigQuery restricts the use of shared Google Cloud resources with [quotas and limits](/bigquery/quotas), including limitations on certain table operations or the number of jobs run within a day.

When you use the clustered table feature with a partitioned table, you are subject to the [limits on partitioned tables](/bigquery/quotas#partitioned_tables).

Quotas and limits also apply to the different types of jobs that you can run against clustered tables. For information about the job quotas that apply to your tables, see [Jobs](/bigquery/quotas#jobs) in "Quotas and Limits".

Clustered table pricing
-----------------------

When you create and use clustered tables in BigQuery, your charges are based on how much data is stored in the tables and on the queries that you run against the data. For more information, see [Storage pricing](/bigquery/pricing#storage) and [Query pricing](/bigquery/pricing#analysis_pricing_models).

Like other BigQuery table operations, clustered table operations take advantage of BigQuery free operations such as batch load, table copy, automatic reclustering, and data export. These operations are subject to [BigQuery quotas and limits](/bigquery/quotas). For information about free operations, see [Free operations](/bigquery/pricing#free).

For a detailed clustered table pricing example, see [Estimate storage and query costs](/bigquery/docs/estimate-costs#clustered_table_pricing_example).

Table security
--------------

To control access to tables in BigQuery, see [Control access to resources with IAM](/bigquery/docs/control-access-to-resources-iam).

What's next
-----------

*   To learn how to create and use clustered tables, see [Creating and using clustered tables](/bigquery/docs/creating-clustered-tables).
*   For information about querying clustered tables, see [Querying clustered tables](/bigquery/docs/querying-clustered-tables).

Was this helpful?

Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-08-07 UTC.

*   ### Why Google
    
    *   [Choosing Google Cloud](/why-google-cloud/)
    *   [Trust and security](/trust-center/)
    *   [Modern Infrastructure Cloud](/solutions/modern-infrastructure/)
    *   [Multicloud](/multicloud/)
    *   [Global infrastructure](/infrastructure/)
    *   [Customers and case studies](/customers/)
    *   [Analyst reports](/analyst-reports/)
    *   [Whitepapers](/whitepapers/)
*   ### Products and pricing
    
    *   [See all products](/products/)
    *   [See all solutions](/solutions/)
    *   [Google Cloud for Startups](/startup/)
    *   [Google Cloud Marketplace](/marketplace/)
    *   [Google Cloud pricing](/pricing/)
    *   [Contact sales](/contact/)
*   ### Support
    
    *   [Google Cloud Community](//www.googlecloudcommunity.com/)
    *   [Support](/support-hub/)
    *   [Release Notes](/release-notes)
    *   [System status](//status.cloud.google.com)
*   ### Resources
    
    *   [GitHub](//github.com/googlecloudPlatform/)
    *   [Getting Started with Google Cloud](/docs/get-started/)
    *   [Google Cloud documentation](/docs/)
    *   [Code samples](/docs/samples)
    *   [Cloud Architecture Center](/architecture/)
    *   [Training and Certification](//cloud.google.com/learn/training/)
    *   [Developer Center](/developers/)
*   ### Engage
    
    *   [Blog](//cloud.google.com/blog/)
    *   [Events](/events/)
    *   [X (Twitter)](//x.com/googlecloud)
    *   [Google Cloud on YouTube](//www.youtube.com/googlecloud)
    *   [Google Cloud Tech on YouTube](//www.youtube.com/googlecloudplatform)
    *   [Become a Partner](/partners/become-a-partner/)
    *   [Google Cloud Affiliate Program](/affiliate-program/)
    *   [Press Corner](//www.googlecloudpresscorner.com/)

*   [About Google](//about.google/)
*   [Privacy](//policies.google.com/privacy)
*   [Site terms](//policies.google.com/terms?hl=en)
*   [Google Cloud terms](/product-terms/)
*   [Manage cookies](#)
*   [Our third decade of climate action: join us](//cloud.google.com/sustainability)
*   Sign up for the Google Cloud newsletter [Subscribe](//cloud.google.com/newsletter/)

*   [English](https://cloud.google.com/bigquery/docs/clustered-tables)
*   [Deutsch](https://cloud.google.com/bigquery/docs/clustered-tables?hl=de)
*   [Español – América Latina](https://cloud.google.com/bigquery/docs/clustered-tables?hl=es-419)
*   [Français](https://cloud.google.com/bigquery/docs/clustered-tables?hl=fr)
*   [Indonesia](https://cloud.google.com/bigquery/docs/clustered-tables?hl=id)
*   [Italiano](https://cloud.google.com/bigquery/docs/clustered-tables?hl=it)
*   [Português – Brasil](https://cloud.google.com/bigquery/docs/clustered-tables?hl=pt-br)
*   [中文 – 简体](https://cloud.google.com/bigquery/docs/clustered-tables?hl=zh-cn)
*   [中文 – 繁體](https://cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)
*   [日本語](https://cloud.google.com/bigquery/docs/clustered-tables?hl=ja)
*   [한국어](https://cloud.google.com/bigquery/docs/clustered-tables?hl=ko)

close

### Welcome to Cloud Shell

Cloud Shell is a development environment that you can use in the browser:

*   Activate Cloud Shell to explore Google Cloud with a terminal and an editor
*   Start a free trial to get $300 in free credits

Activate Cloud Shell Start a free trial

![](https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/images/cloud-shell-cta-art.png)

\[\] {&#34;at&#34;: &#34;True&#34;, &#34;ga4&#34;: \[\], &#34;ga4p&#34;: \[\], &#34;gtm&#34;: \[{&#34;id&#34;: &#34;GTM-5CVQBG&#34;, &#34;purpose&#34;: 1}\], &#34;parameters&#34;: {&#34;internalUser&#34;: &#34;False&#34;, &#34;language&#34;: {&#34;machineTranslated&#34;: &#34;False&#34;, &#34;requested&#34;: &#34;en&#34;, &#34;served&#34;: &#34;en&#34;}, &#34;pageType&#34;: &#34;article&#34;, &#34;projectName&#34;: &#34;BigQuery&#34;, &#34;signedIn&#34;: &#34;True&#34;, &#34;tenant&#34;: &#34;cloud&#34;, &#34;recommendations&#34;: {&#34;sourcePage&#34;: &#34;&#34;, &#34;sourceType&#34;: 0, &#34;sourceRank&#34;: 0, &#34;sourceIdenticalDescriptions&#34;: 0, &#34;sourceTitleWords&#34;: 0, &#34;sourceDescriptionWords&#34;: 0, &#34;experiment&#34;: &#34;&#34;}, &#34;experiment&#34;: {&#34;ids&#34;: &#34;&#34;}}} (function(d,e,v,s,i,t,E){d\['GoogleDevelopersObject'\]=i; t=e.createElement(v);t.async=1;t.src=s;E=e.getElementsByTagName(v)\[0\]; E.parentNode.insertBefore(t,E);})(window, document, 'script', 'https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/js/app\_loader.js', '\[2,"en",null,"/js/devsite\_app\_module.js","https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7","https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud","https://cloud-dot-devsite-v2-prod.appspot.com",null,null,\["/\_pwa/cloud/manifest.json","https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/images/video-placeholder.svg","https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/images/favicons/onecloud/favicon.ico","https://www.gstatic.com/devrel-devsite/prod/v80eb94e0352d656ad1e20abf6117cdec6c1343c7722ef10f52a1a3f77f1e58f7/cloud/images/cloud-logo.svg","https://fonts.googleapis.com/css?family=Google+Sans:400,500,700|Google+Sans+Text:400,400italic,500,500italic,700,700italic|Roboto:400,400italic,500,500italic,700,700italic|Roboto+Mono:400,500,700&display=swap"\],1,null,\[1,6,8,12,14,17,21,25,50,52,63,70,75,76,80,87,91,92,93,97,98,100,101,102,103,104,105,107,108,109,110,112,113,116,117,118,120,122,124,125,126,127,129,130,131,132,133,134,135,136,138,140,141,147,148,149,151,152,156,157,158,159,161,163,164,168,169,170,179,180,182,183,186,191,193,196\],"AIzaSyAP-jjEJBzmIyKR4F-3XITp8yM9T1gEEI8","AIzaSyB6xiKGDR5O3Ak2okS4rLkauxGUG7XP0hg","cloud.google.com","AIzaSyAQk0fBONSGUqCNznf6Krs82Ap1-NV6J4o","AIzaSyCCxcqdrZ\_7QMeLCRY20bh\_SXdAYqy70KY",null,null,null,\["Cloud\_\_cache\_serialized\_dynamic\_content","Profiles\_\_enable\_public\_developer\_profiles","Search\_\_enable\_ai\_search\_summaries","Profiles\_\_enable\_callout\_notifications","MiscFeatureFlags\_\_developers\_footer\_dark\_image","Profiles\_\_enable\_developer\_profile\_benefits\_ui\_redesign","Cloud\_\_enable\_cloudx\_experiment\_ids","Concierge\_\_enable\_tutorial\_this\_code","DevPro\_\_enable\_code\_assist","Profiles\_\_enable\_join\_program\_group\_endpoint","DevPro\_\_enable\_google\_payments","Profiles\_\_enable\_playlist\_community\_acl","Cloud\_\_enable\_cloud\_shell\_fte\_user\_flow","BookNav\_\_enable\_tenant\_cache\_key","DevPro\_\_remove\_eu\_tax\_intake\_form","MiscFeatureFlags\_\_enable\_framebox\_badge\_methods","DevPro\_\_enable\_devpro\_offers","Profiles\_\_enable\_purchase\_prompts","Concierge\_\_enable\_remove\_info\_panel\_tags","MiscFeatureFlags\_\_enable\_project\_variables","MiscFeatureFlags\_\_enable\_variable\_operator","Search\_\_enable\_ai\_eligibility\_checks","Profiles\_\_enable\_completecodelab\_endpoint","Cloud\_\_fast\_free\_trial","DevPro\_\_enable\_free\_benefits","DevPro\_\_enable\_nvidia\_credits\_card","DevPro\_\_enable\_developer\_subscriptions","CloudShell\_\_cloud\_code\_overflow\_menu","Cloud\_\_enable\_free\_trial\_server\_call","Search\_\_enable\_ai\_search\_summaries\_restricted","Profiles\_\_enable\_developer\_profiles\_callout","DevPro\_\_enable\_google\_payments\_buyflow","MiscFeatureFlags\_\_enable\_explain\_this\_code","Cloud\_\_enable\_cloud\_dlp\_service","Analytics\_\_enable\_clearcut\_logging","Search\_\_enable\_dynamic\_content\_confidential\_banner","Cloud\_\_enable\_llm\_concierge\_chat","Concierge\_\_enable\_pushui","Search\_\_enable\_ai\_search\_summaries\_for\_all","DevPro\_\_enable\_embed\_profile\_creation","Concierge\_\_enable\_actions\_menu","Profiles\_\_enable\_profile\_collections","DevPro\_\_enable\_firebase\_workspaces\_card","DevPro\_\_enable\_enterprise","MiscFeatureFlags\_\_enable\_firebase\_utm","MiscFeatureFlags\_\_enable\_explicit\_template\_dependencies","Profiles\_\_enable\_dashboard\_curated\_recommendations","Profiles\_\_enable\_release\_notes\_notifications","MiscFeatureFlags\_\_developers\_footer\_image","Profiles\_\_enable\_awarding\_url","DevPro\_\_enable\_vertex\_credit\_card","MiscFeatureFlags\_\_enable\_appearance\_cookies","Search\_\_enable\_page\_map","Profiles\_\_enable\_complete\_playlist\_endpoint","EngEduTelemetry\_\_enable\_engedu\_telemetry","TpcFeatures\_\_enable\_unmirrored\_page\_left\_nav","Profiles\_\_enable\_page\_saving","CloudShell\_\_cloud\_shell\_button","Experiments\_\_reqs\_query\_experiments","Profiles\_\_require\_profile\_eligibility\_for\_signin","DevPro\_\_enable\_google\_one\_card","Profiles\_\_enable\_recognition\_badges","MiscFeatureFlags\_\_gdp\_dashboard\_reskin\_enabled","Cloud\_\_enable\_legacy\_calculator\_redirect","MiscFeatureFlags\_\_enable\_variable\_operator\_index\_yaml","MiscFeatureFlags\_\_emergency\_css","Profiles\_\_enable\_stripe\_subscription\_management","Profiles\_\_enable\_user\_type","DevPro\_\_enable\_cloud\_innovators\_plus","Concierge\_\_enable\_concierge\_restricted","TpcFeatures\_\_proxy\_prod\_host","Cloud\_\_enable\_cloud\_shell","Search\_\_enable\_suggestions\_from\_borg","MiscFeatureFlags\_\_enable\_view\_transitions","Search\_\_scope\_to\_project\_tenant"\],null,null,"AIzaSyBLEMok-5suZ67qRPzx0qUtbnLmyT\_kCVE","https://developerscontentserving-pa.clients6.google.com","AIzaSyCM4QpTRSqP5qI4Dvjt4OAScIN8sOUlO-k","https://developerscontentsearch-pa.clients6.google.com",1,4,1,"https://developerprofiles-pa.clients6.google.com",\[2,"cloud","Google Cloud","cloud.google.com",null,"cloud-dot-devsite-v2-prod.appspot.com",null,null,\[1,1,null,null,null,null,null,null,null,null,null,\[1\],null,null,null,null,null,1,\[1\],\[null,null,null,\[1,20\],"/terms/recommendations"\],\[1\],null,\[1\],\[1,null,1\],\[1,1,null,null,1,null,\["/vertex-ai/"\]\],\[1\]\],null,\[22,null,null,null,null,null,"/images/cloud-logo.svg","/images/favicons/onecloud/apple-icon.png",null,null,null,null,1,1,1,\[6,5\],\[\],null,null,\[\[\],\[\],\[\],\[\],\[\],\[\],\[\],\[\]\],null,null,null,null,null,null,\[\]\],\[\],null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,\[6,1,14,15,22,23,29,37\],null,\[\[null,null,null,null,null,null,\[1,\[\["docType","Choose a content type",\[\["ApiReference",null,null,null,null,null,null,null,null,"API reference"\],\["Sample",null,null,null,null,null,null,null,null,"Code sample"\],\["ReferenceArchitecture",null,null,null,null,null,null,null,null,"Reference architecture"\],\["Tutorial",null,null,null,null,null,null,null,null,"Tutorial"\]\]\],\["category","Choose a topic",\[\["AiAndMachineLearning",null,null,null,null,null,null,null,null,"Artificial intelligence and machine learning (AI/ML)"\],\["ApplicationDevelopment",null,null,null,null,null,null,null,null,"Application development"\],\["BigDataAndAnalytics",null,null,null,null,null,null,null,null,"Big data and analytics"\],\["Compute",null,null,null,null,null,null,null,null,"Compute"\],\["Containers",null,null,null,null,null,null,null,null,"Containers"\],\["Databases",null,null,null,null,null,null,null,null,"Databases"\],\["HybridCloud",null,null,null,null,null,null,null,null,"Hybrid and multicloud"\],\["LoggingAndMonitoring",null,null,null,null,null,null,null,null,"Logging and monitoring"\],\["Migrations",null,null,null,null,null,null,null,null,"Migrations"\],\["Networking",null,null,null,null,null,null,null,null,"Networking"\],\["SecurityAndCompliance",null,null,null,null,null,null,null,null,"Security and compliance"\],\["Serverless",null,null,null,null,null,null,null,null,"Serverless"\],\["Storage",null,null,null,null,null,null,null,null,"Storage"\]\]\]\]\]\],\[1\],null,1\],\[\[null,null,null,null,null,\["GTM-5CVQBG"\],null,null,null,null,null,\[\["GTM-5CVQBG",2\]\],1\],null,null,null,null,null,1\],"mwETRvWii0eU5NUYprb0Y9z5GVbc",4,null,null,null,null,null,null,null,null,null,null,null,null,null,"cloud.devsite.google"\],null,"pk\_live\_5170syrHvgGVmSx9sBrnWtA5luvk9BwnVcvIi7HizpwauFG96WedXsuXh790rtij9AmGllqPtMLfhe2RSwD6Pn38V00uBCydV4m",1,1,"https://developerscontentinsights-pa.clients6.google.com","AIzaSyCg-ZUslalsEbXMfIo9ZP8qufZgo3LSBDU","AIzaSyDxT0vkxnY\_KeINtA4LSePJO-4MAZPMRsE","https://developers.clients6.google.com"\]')