"use strict";(self.webpackChunk_jupyterlite_robolite_kernel_extension=self.webpackChunk_jupyterlite_robolite_kernel_extension||[]).push([[496],{496:(e,r,t)=>{t.r(r),t.d(r,{default:()=>n});var a=t(732),o=t(698);const l=t.p+"68278575914e7ddf8edfdb0588cd127d0e6728ad9ea7f0880a971269c96ea467.png",i="@jupyterlite/robolite-kernel-extension:kernel",n=[{id:i,autoStart:!0,requires:[o.IKernelSpecs],activate:(e,r)=>{const o=JSON.parse(a.PageConfig.getOption("litePluginSettings")||"{}")[i]||{},n=o.pyodideUrl||"https://cdn.jsdelivr.net/pyodide/v0.19.1/full/pyodide.js",s=a.URLExt.parse(n).href,p=(o.pipliteUrls||[]).map((e=>a.URLExt.parse(e).href)),d=!!o.disablePyPIFallback;r.register({spec:{name:"Robot Framework",display_name:"Robot Framework",language:"robotframework",argv:[],spec:{argv:[],env:{},display_name:"Robot Framework",language:"robotframework",interrupt_mode:"message",metadata:{}},resources:{"logo-64x64":l}},create:async e=>{const{RoboliteKernel:r}=await t.e(931).then(t.t.bind(t,931,23));return new r({...e,pyodideUrl:s,pipliteUrls:p,disablePyPIFallback:d})}})}}]}}]);