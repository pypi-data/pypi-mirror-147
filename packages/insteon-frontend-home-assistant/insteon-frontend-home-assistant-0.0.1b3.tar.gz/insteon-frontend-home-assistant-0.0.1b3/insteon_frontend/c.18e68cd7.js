import{u as e,v as t,w as i,x as n,y as o,e as s,t as a,s as r,R as c,$ as l,z as d,r as h,n as p,A as u,B as m,C as _,E as b,F as f,G as g,P as v,h as y,d as x,I as k,J as w,_ as E,K as I,L as C,i as S,M as T,N as A,f as R,O,j as F,k as z,Q as M,S as L,T as D,l as B,U as $,V as P,W as N,X as H,Y as V,Z as U,a0 as K,a1 as W,a2 as G}from"./main-ff869e06.js";function j(i,n,o){let s,a=i;return"object"==typeof i?(a=i.slot,s=i):s={flatten:n},o?e({slot:a,flatten:n,selector:o}):t({descriptor:e=>({get(){var e,t;const i="slot"+(a?`[name=${a}]`:":not([name])"),n=null===(e=this.renderRoot)||void 0===e?void 0:e.querySelector(i);return null!==(t=null==n?void 0:n.assignedNodes(s))&&void 0!==t?t:[]},enumerable:!0,configurable:!0})})}const q=e=>(t,i)=>{if(t.constructor._observers){if(!t.constructor.hasOwnProperty("_observers")){const e=t.constructor._observers;t.constructor._observers=new Map,e.forEach((e,i)=>t.constructor._observers.set(i,e))}}else{t.constructor._observers=new Map;const e=t.updated;t.updated=function(t){e.call(this,t),t.forEach((e,t)=>{const i=this.constructor._observers.get(t);void 0!==i&&i.call(this,this[t],e)})}}t.constructor._observers.set(i,e)};class X extends r{constructor(){super(...arguments),this.value="",this.group=null,this.tabindex=-1,this.disabled=!1,this.twoline=!1,this.activated=!1,this.graphic=null,this.multipleGraphics=!1,this.hasMeta=!1,this.noninteractive=!1,this.selected=!1,this.shouldRenderRipple=!1,this._managingList=null,this.boundOnClick=this.onClick.bind(this),this._firstChanged=!0,this._skipPropRequest=!1,this.rippleHandlers=new c(()=>(this.shouldRenderRipple=!0,this.ripple)),this.listeners=[{target:this,eventNames:["click"],cb:()=>{this.onClick()}},{target:this,eventNames:["mouseenter"],cb:this.rippleHandlers.startHover},{target:this,eventNames:["mouseleave"],cb:this.rippleHandlers.endHover},{target:this,eventNames:["focus"],cb:this.rippleHandlers.startFocus},{target:this,eventNames:["blur"],cb:this.rippleHandlers.endFocus},{target:this,eventNames:["mousedown","touchstart"],cb:e=>{const t=e.type;this.onDown("mousedown"===t?"mouseup":"touchend",e)}}]}get text(){const e=this.textContent;return e?e.trim():""}render(){const e=this.renderText(),t=this.graphic?this.renderGraphic():l``,i=this.hasMeta?this.renderMeta():l``;return l`
      ${this.renderRipple()}
      ${t}
      ${e}
      ${i}`}renderRipple(){return this.shouldRenderRipple?l`
      <mwc-ripple
        .activated=${this.activated}>
      </mwc-ripple>`:this.activated?l`<div class="fake-activated-ripple"></div>`:""}renderGraphic(){const e={multi:this.multipleGraphics};return l`
      <span class="mdc-deprecated-list-item__graphic material-icons ${d(e)}">
        <slot name="graphic"></slot>
      </span>`}renderMeta(){return l`
      <span class="mdc-deprecated-list-item__meta material-icons">
        <slot name="meta"></slot>
      </span>`}renderText(){const e=this.twoline?this.renderTwoline():this.renderSingleLine();return l`
      <span class="mdc-deprecated-list-item__text">
        ${e}
      </span>`}renderSingleLine(){return l`<slot></slot>`}renderTwoline(){return l`
      <span class="mdc-deprecated-list-item__primary-text">
        <slot></slot>
      </span>
      <span class="mdc-deprecated-list-item__secondary-text">
        <slot name="secondary"></slot>
      </span>
    `}onClick(){this.fireRequestSelected(!this.selected,"interaction")}onDown(e,t){const i=()=>{window.removeEventListener(e,i),this.rippleHandlers.endPress()};window.addEventListener(e,i),this.rippleHandlers.startPress(t)}fireRequestSelected(e,t){if(this.noninteractive)return;const i=new CustomEvent("request-selected",{bubbles:!0,composed:!0,detail:{source:t,selected:e}});this.dispatchEvent(i)}connectedCallback(){super.connectedCallback(),this.noninteractive||this.setAttribute("mwc-list-item","");for(const e of this.listeners)for(const t of e.eventNames)e.target.addEventListener(t,e.cb,{passive:!0})}disconnectedCallback(){super.disconnectedCallback();for(const e of this.listeners)for(const t of e.eventNames)e.target.removeEventListener(t,e.cb);this._managingList&&(this._managingList.debouncedLayout?this._managingList.debouncedLayout(!0):this._managingList.layout(!0))}firstUpdated(){const e=new Event("list-item-rendered",{bubbles:!0,composed:!0});this.dispatchEvent(e)}}i([n("slot")],X.prototype,"slotElement",void 0),i([o("mwc-ripple")],X.prototype,"ripple",void 0),i([s({type:String})],X.prototype,"value",void 0),i([s({type:String,reflect:!0})],X.prototype,"group",void 0),i([s({type:Number,reflect:!0})],X.prototype,"tabindex",void 0),i([s({type:Boolean,reflect:!0}),q((function(e){e?this.setAttribute("aria-disabled","true"):this.setAttribute("aria-disabled","false")}))],X.prototype,"disabled",void 0),i([s({type:Boolean,reflect:!0})],X.prototype,"twoline",void 0),i([s({type:Boolean,reflect:!0})],X.prototype,"activated",void 0),i([s({type:String,reflect:!0})],X.prototype,"graphic",void 0),i([s({type:Boolean})],X.prototype,"multipleGraphics",void 0),i([s({type:Boolean})],X.prototype,"hasMeta",void 0),i([s({type:Boolean,reflect:!0}),q((function(e){e?(this.removeAttribute("aria-checked"),this.removeAttribute("mwc-list-item"),this.selected=!1,this.activated=!1,this.tabIndex=-1):this.setAttribute("mwc-list-item","")}))],X.prototype,"noninteractive",void 0),i([s({type:Boolean,reflect:!0}),q((function(e){const t=this.getAttribute("role"),i="gridcell"===t||"option"===t||"row"===t||"tab"===t;i&&e?this.setAttribute("aria-selected","true"):i&&this.setAttribute("aria-selected","false"),this._firstChanged?this._firstChanged=!1:this._skipPropRequest||this.fireRequestSelected(e,"property")}))],X.prototype,"selected",void 0),i([a()],X.prototype,"shouldRenderRipple",void 0),i([a()],X.prototype,"_managingList",void 0);const Q=h`:host{cursor:pointer;user-select:none;-webkit-tap-highlight-color:transparent;height:48px;display:flex;position:relative;align-items:center;justify-content:flex-start;overflow:hidden;padding:0;padding-left:var(--mdc-list-side-padding, 16px);padding-right:var(--mdc-list-side-padding, 16px);outline:none;height:48px;color:rgba(0,0,0,.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87))}:host:focus{outline:none}:host([activated]){color:#6200ee;color:var(--mdc-theme-primary, #6200ee);--mdc-ripple-color: var( --mdc-theme-primary, #6200ee )}:host([activated]) .mdc-deprecated-list-item__graphic{color:#6200ee;color:var(--mdc-theme-primary, #6200ee)}:host([activated]) .fake-activated-ripple::before{position:absolute;display:block;top:0;bottom:0;left:0;right:0;width:100%;height:100%;pointer-events:none;z-index:1;content:"";opacity:0.12;opacity:var(--mdc-ripple-activated-opacity, 0.12);background-color:#6200ee;background-color:var(--mdc-ripple-color, var(--mdc-theme-primary, #6200ee))}.mdc-deprecated-list-item__graphic{flex-shrink:0;align-items:center;justify-content:center;fill:currentColor;display:inline-flex}.mdc-deprecated-list-item__graphic ::slotted(*){flex-shrink:0;align-items:center;justify-content:center;fill:currentColor;width:100%;height:100%;text-align:center}.mdc-deprecated-list-item__meta{width:var(--mdc-list-item-meta-size, 24px);height:var(--mdc-list-item-meta-size, 24px);margin-left:auto;margin-right:0;color:rgba(0, 0, 0, 0.38);color:var(--mdc-theme-text-hint-on-background, rgba(0, 0, 0, 0.38))}.mdc-deprecated-list-item__meta.multi{width:auto}.mdc-deprecated-list-item__meta ::slotted(*){width:var(--mdc-list-item-meta-size, 24px);line-height:var(--mdc-list-item-meta-size, 24px)}.mdc-deprecated-list-item__meta ::slotted(.material-icons),.mdc-deprecated-list-item__meta ::slotted(mwc-icon){line-height:var(--mdc-list-item-meta-size, 24px) !important}.mdc-deprecated-list-item__meta ::slotted(:not(.material-icons):not(mwc-icon)){-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-caption-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.75rem;font-size:var(--mdc-typography-caption-font-size, 0.75rem);line-height:1.25rem;line-height:var(--mdc-typography-caption-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-caption-font-weight, 400);letter-spacing:0.0333333333em;letter-spacing:var(--mdc-typography-caption-letter-spacing, 0.0333333333em);text-decoration:inherit;text-decoration:var(--mdc-typography-caption-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-caption-text-transform, inherit)}[dir=rtl] .mdc-deprecated-list-item__meta,.mdc-deprecated-list-item__meta[dir=rtl]{margin-left:0;margin-right:auto}.mdc-deprecated-list-item__meta ::slotted(*){width:100%;height:100%}.mdc-deprecated-list-item__text{text-overflow:ellipsis;white-space:nowrap;overflow:hidden}.mdc-deprecated-list-item__text ::slotted([for]),.mdc-deprecated-list-item__text[for]{pointer-events:none}.mdc-deprecated-list-item__primary-text{text-overflow:ellipsis;white-space:nowrap;overflow:hidden;display:block;margin-top:0;line-height:normal;margin-bottom:-20px;display:block}.mdc-deprecated-list-item__primary-text::before{display:inline-block;width:0;height:32px;content:"";vertical-align:0}.mdc-deprecated-list-item__primary-text::after{display:inline-block;width:0;height:20px;content:"";vertical-align:-20px}.mdc-deprecated-list-item__secondary-text{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);text-overflow:ellipsis;white-space:nowrap;overflow:hidden;display:block;margin-top:0;line-height:normal;display:block}.mdc-deprecated-list-item__secondary-text::before{display:inline-block;width:0;height:20px;content:"";vertical-align:0}.mdc-deprecated-list--dense .mdc-deprecated-list-item__secondary-text{font-size:inherit}* ::slotted(a),a{color:inherit;text-decoration:none}:host([twoline]){height:72px}:host([twoline]) .mdc-deprecated-list-item__text{align-self:flex-start}:host([disabled]),:host([noninteractive]){cursor:default;pointer-events:none}:host([disabled]) .mdc-deprecated-list-item__text ::slotted(*){opacity:.38}:host([disabled]) .mdc-deprecated-list-item__text ::slotted(*),:host([disabled]) .mdc-deprecated-list-item__primary-text ::slotted(*),:host([disabled]) .mdc-deprecated-list-item__secondary-text ::slotted(*){color:#000;color:var(--mdc-theme-on-surface, #000)}.mdc-deprecated-list-item__secondary-text ::slotted(*){color:rgba(0, 0, 0, 0.54);color:var(--mdc-theme-text-secondary-on-background, rgba(0, 0, 0, 0.54))}.mdc-deprecated-list-item__graphic ::slotted(*){background-color:transparent;color:rgba(0, 0, 0, 0.38);color:var(--mdc-theme-text-icon-on-background, rgba(0, 0, 0, 0.38))}.mdc-deprecated-list-group__subheader ::slotted(*){color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87))}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic{width:var(--mdc-list-item-graphic-size, 40px);height:var(--mdc-list-item-graphic-size, 40px)}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic.multi{width:auto}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(*){width:var(--mdc-list-item-graphic-size, 40px);line-height:var(--mdc-list-item-graphic-size, 40px)}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon){line-height:var(--mdc-list-item-graphic-size, 40px) !important}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(*){border-radius:50%}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic,:host([graphic=medium]) .mdc-deprecated-list-item__graphic,:host([graphic=large]) .mdc-deprecated-list-item__graphic,:host([graphic=control]) .mdc-deprecated-list-item__graphic{margin-left:0;margin-right:var(--mdc-list-item-graphic-margin, 16px)}[dir=rtl] :host([graphic=avatar]) .mdc-deprecated-list-item__graphic,[dir=rtl] :host([graphic=medium]) .mdc-deprecated-list-item__graphic,[dir=rtl] :host([graphic=large]) .mdc-deprecated-list-item__graphic,[dir=rtl] :host([graphic=control]) .mdc-deprecated-list-item__graphic,:host([graphic=avatar]) .mdc-deprecated-list-item__graphic[dir=rtl],:host([graphic=medium]) .mdc-deprecated-list-item__graphic[dir=rtl],:host([graphic=large]) .mdc-deprecated-list-item__graphic[dir=rtl],:host([graphic=control]) .mdc-deprecated-list-item__graphic[dir=rtl]{margin-left:var(--mdc-list-item-graphic-margin, 16px);margin-right:0}:host([graphic=icon]) .mdc-deprecated-list-item__graphic{width:var(--mdc-list-item-graphic-size, 24px);height:var(--mdc-list-item-graphic-size, 24px);margin-left:0;margin-right:var(--mdc-list-item-graphic-margin, 32px)}:host([graphic=icon]) .mdc-deprecated-list-item__graphic.multi{width:auto}:host([graphic=icon]) .mdc-deprecated-list-item__graphic ::slotted(*){width:var(--mdc-list-item-graphic-size, 24px);line-height:var(--mdc-list-item-graphic-size, 24px)}:host([graphic=icon]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=icon]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon){line-height:var(--mdc-list-item-graphic-size, 24px) !important}[dir=rtl] :host([graphic=icon]) .mdc-deprecated-list-item__graphic,:host([graphic=icon]) .mdc-deprecated-list-item__graphic[dir=rtl]{margin-left:var(--mdc-list-item-graphic-margin, 32px);margin-right:0}:host([graphic=avatar]:not([twoLine])),:host([graphic=icon]:not([twoLine])){height:56px}:host([graphic=medium]:not([twoLine])),:host([graphic=large]:not([twoLine])){height:72px}:host([graphic=medium]) .mdc-deprecated-list-item__graphic,:host([graphic=large]) .mdc-deprecated-list-item__graphic{width:var(--mdc-list-item-graphic-size, 56px);height:var(--mdc-list-item-graphic-size, 56px)}:host([graphic=medium]) .mdc-deprecated-list-item__graphic.multi,:host([graphic=large]) .mdc-deprecated-list-item__graphic.multi{width:auto}:host([graphic=medium]) .mdc-deprecated-list-item__graphic ::slotted(*),:host([graphic=large]) .mdc-deprecated-list-item__graphic ::slotted(*){width:var(--mdc-list-item-graphic-size, 56px);line-height:var(--mdc-list-item-graphic-size, 56px)}:host([graphic=medium]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=medium]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon),:host([graphic=large]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=large]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon){line-height:var(--mdc-list-item-graphic-size, 56px) !important}:host([graphic=large]){padding-left:0px}`;let Y=class extends X{};Y.styles=[Q],Y=i([p("mwc-list-item")],Y);const{H:Z}=u,J=e=>void 0===e.strings,ee=()=>document.createComment(""),te=(e,t,i)=>{var n;const o=e._$AA.parentNode,s=void 0===t?e._$AB:t._$AA;if(void 0===i){const t=o.insertBefore(ee(),s),n=o.insertBefore(ee(),s);i=new Z(t,n,e,e.options)}else{const t=i._$AB.nextSibling,a=i._$AM,r=a!==e;if(r){let t;null===(n=i._$AQ)||void 0===n||n.call(i,e),i._$AM=e,void 0!==i._$AP&&(t=e._$AU)!==a._$AU&&i._$AP(t)}if(t!==s||r){let e=i._$AA;for(;e!==t;){const t=e.nextSibling;o.insertBefore(e,s),e=t}}}return i},ie=(e,t,i=e)=>(e._$AI(t,i),e),ne={},oe=(e,t=ne)=>e._$AH=t,se=e=>{var t;null===(t=e._$AP)||void 0===t||t.call(e,!1,!0);let i=e._$AA;const n=e._$AB.nextSibling;for(;i!==n;){const e=i.nextSibling;i.remove(),i=e}},ae=(e,t)=>{var i,n;const o=e._$AN;if(void 0===o)return!1;for(const e of o)null===(n=(i=e)._$AO)||void 0===n||n.call(i,t,!1),ae(e,t);return!0},re=e=>{let t,i;do{if(void 0===(t=e._$AM))break;i=t._$AN,i.delete(e),e=t}while(0===(null==i?void 0:i.size))},ce=e=>{for(let t;t=e._$AM;e=t){let i=t._$AN;if(void 0===i)t._$AN=i=new Set;else if(i.has(e))break;i.add(e),he(t)}};function le(e){void 0!==this._$AN?(re(this),this._$AM=e,ce(this)):this._$AM=e}function de(e,t=!1,i=0){const n=this._$AH,o=this._$AN;if(void 0!==o&&0!==o.size)if(t)if(Array.isArray(n))for(let e=i;e<n.length;e++)ae(n[e],!1),re(n[e]);else null!=n&&(ae(n,!1),re(n));else ae(this,e)}const he=e=>{var t,i,n,o;e.type==_.CHILD&&(null!==(t=(n=e)._$AP)&&void 0!==t||(n._$AP=de),null!==(i=(o=e)._$AQ)&&void 0!==i||(o._$AQ=le))};class pe extends m{constructor(){super(...arguments),this._$AN=void 0}_$AT(e,t,i){super._$AT(e,t,i),ce(this),this.isConnected=e._$AU}_$AO(e,t=!0){var i,n;e!==this.isConnected&&(this.isConnected=e,e?null===(i=this.reconnected)||void 0===i||i.call(this):null===(n=this.disconnected)||void 0===n||n.call(this)),t&&(ae(this,e),re(this))}setValue(e){if(J(this._$Ct))this._$Ct._$AI(e,this);else{const t=[...this._$Ct._$AH];t[this._$Ci]=e,this._$Ct._$AI(t,this,0)}}disconnected(){}reconnected(){}}const ue=(e,t,i)=>{const n=new Map;for(let o=t;o<=i;o++)n.set(e[o],o);return n},me=b(class extends m{constructor(e){if(super(e),e.type!==_.CHILD)throw Error("repeat() can only be used in text expressions")}dt(e,t,i){let n;void 0===i?i=t:void 0!==t&&(n=t);const o=[],s=[];let a=0;for(const t of e)o[a]=n?n(t,a):a,s[a]=i(t,a),a++;return{values:s,keys:o}}render(e,t,i){return this.dt(e,t,i).values}update(e,[t,i,n]){var o;const s=(e=>e._$AH)(e),{values:a,keys:r}=this.dt(t,i,n);if(!Array.isArray(s))return this.at=r,a;const c=null!==(o=this.at)&&void 0!==o?o:this.at=[],l=[];let d,h,p=0,u=s.length-1,m=0,_=a.length-1;for(;p<=u&&m<=_;)if(null===s[p])p++;else if(null===s[u])u--;else if(c[p]===r[m])l[m]=ie(s[p],a[m]),p++,m++;else if(c[u]===r[_])l[_]=ie(s[u],a[_]),u--,_--;else if(c[p]===r[_])l[_]=ie(s[p],a[_]),te(e,l[_+1],s[p]),p++,_--;else if(c[u]===r[m])l[m]=ie(s[u],a[m]),te(e,s[p],s[u]),u--,m++;else if(void 0===d&&(d=ue(r,m,_),h=ue(c,p,u)),d.has(c[p]))if(d.has(c[u])){const t=h.get(r[m]),i=void 0!==t?s[t]:null;if(null===i){const t=te(e,s[p]);ie(t,a[m]),l[m]=t}else l[m]=ie(i,a[m]),te(e,s[p],i),s[t]=null;m++}else se(s[u]),u--;else se(s[p]),p++;for(;m<=_;){const t=te(e,l[_+1]);ie(t,a[m]),l[m++]=t}for(;p<=u;){const e=s[p++];null!==e&&se(e)}return this.at=r,oe(e,l),f}});let _e,be;async function fe(){return be||async function(){if(_e)return(await _e).default;_e=window.ResizeObserver;try{new _e((function(){}))}catch(e){_e=import("./c.fe385c94.js"),_e=(await _e).default}return be=_e}()}const ge=Symbol("scrollerRef");let ve="attachShadow"in Element.prototype&&(!("ShadyDOM"in window)||!window.ShadyDOM.inUse);let ye=null;function xe(e,t){return`\n    ${e} {\n      display: block;\n      position: relative;\n      contain: strict;\n      height: 150px;\n      overflow: auto;\n    }\n    ${t} {\n      box-sizing: border-box;\n    }`}class ke{constructor(e){this._benchmarkStart=null,this._layout=null,this._scrollTarget=null,this._sizer=null,this._scrollSize=null,this._scrollErr=null,this._childrenPos=null,this._childMeasurements=null,this._toBeMeasured=new Map,this._rangeChanged=!0,this._itemsChanged=!0,this._visibilityChanged=!0,this._container=null,this._containerElement=null,this._containerInlineStyle=null,this._containerStylesheet=null,this._containerSize=null,this._containerRO=null,this._childrenRO=null,this._mutationObserver=null,this._mutationPromise=null,this._mutationPromiseResolver=null,this._mutationsObserved=!1,this._loadListener=this._childLoaded.bind(this),this._scrollToIndex=null,this._items=[],this._totalItems=null,this._first=0,this._last=0,this._scheduled=new WeakSet,this._measureCallback=null,this._measureChildOverride=null,this._first=-1,this._last=-1,e&&Object.assign(this,e)}set items(e){e!==this._items&&(this._itemsChanged=!0,this._items=e,this._schedule(this._updateLayout))}get totalItems(){return null===this._totalItems?this._items.length:this._totalItems}set totalItems(e){if("number"!=typeof e&&null!==e)throw new Error("New value must be a number.");e!==this._totalItems&&(this._totalItems=e,this._schedule(this._updateLayout))}get container(){return this._container}set container(e){e!==this._container&&(this._container&&this._children.forEach(e=>e.parentNode.removeChild(e)),this._container=e,this._schedule(this._updateLayout),this._initResizeObservers().then(()=>{const t=this._containerElement,i=e&&e.nodeType===Node.DOCUMENT_FRAGMENT_NODE?e.host:e;t!==i&&(this._containerRO.disconnect(),this._containerSize=null,t?(this._containerInlineStyle?t.setAttribute("style",this._containerInlineStyle):t.removeAttribute("style"),this._containerInlineStyle=null,t===this._scrollTarget&&(t.removeEventListener("scroll",this,{passive:!0}),this._sizer&&this._sizer.remove()),t.removeEventListener("load",this._loadListener,!0),this._mutationObserver.disconnect()):addEventListener("scroll",this,{passive:!0}),this._containerElement=i,i&&(this._containerInlineStyle=i.getAttribute("style")||null,this._applyContainerStyles(),i===this._scrollTarget&&(this._sizer=this._sizer||this._createContainerSizer(),this._container.insertBefore(this._sizer,this._container.firstChild)),this._schedule(this._updateLayout),this._containerRO.observe(i),this._mutationObserver.observe(i,{childList:!0}),this._mutationPromise=new Promise(e=>this._mutationPromiseResolver=e),this._layout&&this._layout.listenForChildLoadEvents&&i.addEventListener("load",this._loadListener,!0)))}))}get layout(){return this._layout}set layout(e){if(this._layout===e)return;let t,i;if("object"==typeof e?(void 0!==e.type&&(t=e.type,delete e.type),i=e):t=e,"function"==typeof t){if(this._layout instanceof t)return void(i&&(this._layout.config=i));t=new t(i)}this._layout&&(this._measureCallback=null,this._measureChildOverride=null,this._layout.removeEventListener("scrollsizechange",this),this._layout.removeEventListener("scrollerrorchange",this),this._layout.removeEventListener("itempositionchange",this),this._layout.removeEventListener("rangechange",this),delete this.container[ge],this.container.removeEventListener("load",this._loadListener,!0),this._containerElement&&this._sizeContainer(void 0)),this._layout=t,this._layout&&(this._layout.measureChildren&&"function"==typeof this._layout.updateItemSizes&&("function"==typeof this._layout.measureChildren&&(this._measureChildOverride=this._layout.measureChildren),this._measureCallback=this._layout.updateItemSizes.bind(this._layout)),this._layout.addEventListener("scrollsizechange",this),this._layout.addEventListener("scrollerrorchange",this),this._layout.addEventListener("itempositionchange",this),this._layout.addEventListener("rangechange",this),this._container[ge]=this,this._layout.listenForChildLoadEvents&&this._container.addEventListener("load",this._loadListener,!0),this._schedule(this._updateLayout))}startBenchmarking(){null===this._benchmarkStart&&(this._benchmarkStart=window.performance.now())}stopBenchmarking(){if(null!==this._benchmarkStart){const e=window.performance.now(),t=e-this._benchmarkStart,i=performance.getEntriesByName("uv-virtualizing","measure").filter(t=>t.startTime>=this._benchmarkStart&&t.startTime<e).reduce((e,t)=>e+t.duration,0);return this._benchmarkStart=null,{timeElapsed:t,virtualizationTime:i}}return null}_measureChildren(){const e={},t=this._children,i=this._measureChildOverride||this._measureChild;for(let n=0;n<t.length;n++){const o=t[n],s=this._first+n;(this._itemsChanged||this._toBeMeasured.has(o))&&(e[s]=i.call(this,o,this._items[s]))}this._childMeasurements=e,this._schedule(this._updateLayout),this._toBeMeasured.clear()}_measureChild(e){const{width:t,height:i}=e.getBoundingClientRect();return Object.assign({width:t,height:i},function(e){const t=window.getComputedStyle(e);return{marginTop:we(t.marginTop),marginRight:we(t.marginRight),marginBottom:we(t.marginBottom),marginLeft:we(t.marginLeft)}}(e))}get scrollTarget(){return this._scrollTarget}set scrollTarget(e){e===window&&(e=null),this._scrollTarget!==e&&(this._sizeContainer(void 0),this._scrollTarget&&(this._scrollTarget.removeEventListener("scroll",this,{passive:!0}),this._sizer&&this._scrollTarget===this._containerElement&&this._sizer.remove()),this._scrollTarget=e,e&&(e.addEventListener("scroll",this,{passive:!0}),e===this._containerElement&&(this._sizer=this._sizer||this._createContainerSizer(),this._container.insertBefore(this._sizer,this._container.firstChild))))}set scrollToIndex(e){this._scrollToIndex=e,this._schedule(this._updateLayout)}async _schedule(e){this._scheduled.has(e)||(this._scheduled.add(e),await Promise.resolve(),this._scheduled.delete(e),e.call(this))}async _updateDOM(){const{_rangeChanged:e,_itemsChanged:t}=this;this._visibilityChanged&&(this._notifyVisibility(),this._visibilityChanged=!1),(e||t)&&(this._notifyRange(),this._rangeChanged=!1,this._itemsChanged=!1,await this._mutationPromise),this._layout.measureChildren&&this._children.forEach(e=>this._childrenRO.observe(e)),this._positionChildren(this._childrenPos),this._sizeContainer(this._scrollSize),this._scrollErr&&(this._correctScrollError(this._scrollErr),this._scrollErr=null),this._benchmarkStart&&"mark"in window.performance&&window.performance.mark("uv-end")}_updateLayout(){this._layout.totalItems=this._totalItems,null!==this._scrollToIndex&&(this._layout.scrollToIndex(this._scrollToIndex.index,this._scrollToIndex.position),this._scrollToIndex=null),this._updateView(),null!==this._childMeasurements&&(this._measureCallback&&this._measureCallback(this._childMeasurements),this._childMeasurements=null),this._layout.reflowIfNeeded(this._itemsChanged),this._benchmarkStart&&"mark"in window.performance&&window.performance.mark("uv-end")}_handleScrollEvent(){if(this._benchmarkStart&&"mark"in window.performance){try{window.performance.measure("uv-virtualizing","uv-start","uv-end")}catch(e){}window.performance.mark("uv-start")}this._schedule(this._updateLayout)}handleEvent(e){switch(e.type){case"scroll":this._scrollTarget&&e.target!==this._scrollTarget||this._handleScrollEvent();break;case"scrollsizechange":this._scrollSize=e.detail,this._schedule(this._updateDOM);break;case"scrollerrorchange":this._scrollErr=e.detail,this._schedule(this._updateDOM);break;case"itempositionchange":this._childrenPos=e.detail,this._schedule(this._updateDOM);break;case"rangechange":this._adjustRange(e.detail),this._schedule(this._updateDOM);break;default:console.warn("event not handled",e)}}async _initResizeObservers(){if(null===this._containerRO){const e=await fe();this._containerRO=new e(e=>this._containerSizeChanged(e[0].contentRect)),this._childrenRO=new e(this._childrenSizeChanged.bind(this)),this._mutationObserver=new MutationObserver(this._observeMutations.bind(this))}}_applyContainerStyles(){if(ve){if(null===this._containerStylesheet){(this._containerStylesheet=document.createElement("style")).textContent=xe(":host","::slotted(*)")}const e=this._containerElement.shadowRoot||this._containerElement.attachShadow({mode:"open"}),t=e.querySelector("slot:not([name])");e.appendChild(this._containerStylesheet),t||e.appendChild(document.createElement("slot"))}else ye||(ye=document.createElement("style"),ye.textContent=xe(".uni-virtualizer-host",".uni-virtualizer-host > *"),document.head.appendChild(ye)),this._containerElement&&this._containerElement.classList.add("uni-virtualizer-host")}_createContainerSizer(){const e=document.createElement("div");return Object.assign(e.style,{position:"absolute",margin:"-2px 0 0 0",padding:0,visibility:"hidden",fontSize:"2px"}),e.innerHTML="&nbsp;",e.id="uni-virtualizer-spacer",e}get _children(){const e=[];let t=this.container.firstElementChild;for(;t;)"uni-virtualizer-spacer"!==t.id&&e.push(t),t=t.nextElementSibling;return e}_updateView(){if(!this.container||!this._containerElement||!this._layout)return;let e,t,i,n;if(this._scrollTarget===this._containerElement&&null!==this._containerSize)e=this._containerSize.width,t=this._containerSize.height,n=this._containerElement.scrollLeft,i=this._containerElement.scrollTop;else{const o=this._containerElement.getBoundingClientRect(),s=this._scrollTarget?this._scrollTarget.getBoundingClientRect():{top:o.top+window.pageYOffset,left:o.left+window.pageXOffset,width:innerWidth,height:innerHeight},a=s.width,r=s.height,c=Math.max(0,Math.min(a,o.left-s.left)),l=Math.max(0,Math.min(r,o.top-s.top));e=("vertical"===this._layout.direction?Math.max(0,Math.min(a,o.right-s.left)):a)-c,t=("vertical"===this._layout.direction?r:Math.max(0,Math.min(r,o.bottom-s.top)))-l,n=Math.max(0,-(o.left-s.left)),i=Math.max(0,-(o.top-s.top))}this._layout.viewportSize={width:e,height:t},this._layout.viewportScroll={top:i,left:n}}_sizeContainer(e){if(this._scrollTarget===this._containerElement){const t=e&&e.width?e.width-1:0,i=e&&e.height?e.height-1:0;this._sizer&&(this._sizer.style.transform=`translate(${t}px, ${i}px)`)}else if(this._containerElement){const t=this._containerElement.style;t.minWidth=e&&e.width?e.width+"px":null,t.minHeight=e&&e.height?e.height+"px":null}}_positionChildren(e){if(e){const t=this._children;Object.keys(e).forEach(i=>{const n=i-this._first,o=t[n];if(o){const{top:t,left:n,width:s,height:a}=e[i];o.style.position="absolute",o.style.transform=`translate(${n}px, ${t}px)`,void 0!==s&&(o.style.width=s+"px"),void 0!==a&&(o.style.height=a+"px")}})}}async _adjustRange(e){const{_first:t,_last:i,_firstVisible:n,_lastVisible:o}=this;this._first=e.first,this._last=e.last,this._firstVisible=e.firstVisible,this._lastVisible=e.lastVisible,this._rangeChanged=this._rangeChanged||this._first!==t||this._last!==i,this._visibilityChanged=this._visibilityChanged||this._firstVisible!==n||this._lastVisible!==o}_correctScrollError(e){this._scrollTarget?(this._scrollTarget.scrollTop-=e.top,this._scrollTarget.scrollLeft-=e.left):window.scroll(window.pageXOffset-e.left,window.pageYOffset-e.top)}_notifyRange(){this._container.dispatchEvent(new CustomEvent("rangeChanged",{detail:{first:this._first,last:this._last,firstVisible:this._firstVisible,lastVisible:this._lastVisible}}))}_notifyVisibility(){this._container.dispatchEvent(new CustomEvent("visibilityChanged",{detail:{first:this._first,last:this._last,firstVisible:this._firstVisible,lastVisible:this._lastVisible}}))}_containerSizeChanged(e){const{width:t,height:i}=e;this._containerSize={width:t,height:i},this._schedule(this._updateLayout)}async _observeMutations(){this._mutationsObserved||(this._mutationsObserved=!0,this._mutationPromiseResolver(),this._mutationPromise=new Promise(e=>this._mutationPromiseResolver=e),this._mutationsObserved=!1)}_childLoaded(){}_childrenSizeChanged(e){for(let t of e)this._toBeMeasured.set(t.target,t.contentRect);this._measureChildren(),this._schedule(this._updateLayout)}}function we(e){const t=e?parseFloat(e):NaN;return Number.isNaN(t)?0:t}const Ee=e=>e;const Ie=b(class extends pe{constructor(e){if(super(e),this.first=0,this.last=-1,e.type!==_.CHILD)throw new Error("The scroll directive can only be used in child expressions")}render(e){e&&(this.renderItem=e.renderItem,this.keyFunction=e.keyFunction);const t=[];if(this.first>=0&&this.last>=this.first)for(let e=this.first;e<this.last+1;e++)t.push(this.items[e]);return me(t,this.keyFunction||Ee,this.renderItem)}update(e,[t]){var i;if(this.scroller||this._initialize(e,t)){const{scroller:e}=this;return this.items=e.items=t.items,e.totalItems=t.totalItems||(null===(i=t.items)||void 0===i?void 0:i.length)||0,e.layout=t.layout,e.scrollTarget=t.scrollTarget||this.container,t.scrollToIndex&&(e.scrollToIndex=t.scrollToIndex),this.render(t)}return g}_initialize(e,t){const i=this.container=e.parentNode;return i&&1===i.nodeType?(this.scroller=new ke({container:i}),i.addEventListener("rangeChanged",e=>{this.first=e.detail.first,this.last=e.detail.last,this.setValue(this.render())}),!0):(Promise.resolve().then(()=>this.update(e,[t])),!1)}});let Ce,Se;async function Te(){return Se||async function(){Ce=window.EventTarget;try{new Ce}catch(e){Ce=(await import("./c.e4ba960c.js")).EventTarget}return Se=Ce}()}class Ae{constructor(e){this._latestCoords={left:0,top:0},this._direction="vertical",this._viewportSize={width:0,height:0},this._pendingReflow=!1,this._pendingLayoutUpdate=!1,this._scrollToIndex=-1,this._scrollToAnchor=0,this._eventTargetPromise=Te().then(e=>{this._eventTarget=new e}),this._physicalMin=0,this._physicalMax=0,this._first=-1,this._last=-1,this._itemSize={width:100,height:100},this._spacing=0,this._sizeDim="height",this._secondarySizeDim="width",this._positionDim="top",this._secondaryPositionDim="left",this._scrollPosition=0,this._scrollError=0,this._totalItems=0,this._scrollSize=1,this._overhang=1e3,e&&(this.config=e)}set config(e){Object.assign(this,Object.assign({},this.constructor._defaultConfig,e))}get config(){const e={};for(let t in this.constructor._defaultConfig)e[t]=this[t];return e}get totalItems(){return this._totalItems}set totalItems(e){const t=Number(e);t!==this._totalItems&&(this._totalItems=t,this._scheduleReflow())}get direction(){return this._direction}set direction(e){(e="horizontal"===e?e:"vertical")!==this._direction&&(this._direction=e,this._sizeDim="horizontal"===e?"width":"height",this._secondarySizeDim="horizontal"===e?"height":"width",this._positionDim="horizontal"===e?"left":"top",this._secondaryPositionDim="horizontal"===e?"top":"left",this._scheduleLayoutUpdate())}get itemSize(){return this._itemSize}set itemSize(e){const{_itemDim1:t,_itemDim2:i}=this;Object.assign(this._itemSize,e),t===this._itemDim1&&i===this._itemDim2||(i!==this._itemDim2?this._itemDim2Changed():this._scheduleLayoutUpdate())}get spacing(){return this._spacing}set spacing(e){const t=Number(e);t!==this._spacing&&(this._spacing=t,this._scheduleLayoutUpdate())}get viewportSize(){return this._viewportSize}set viewportSize(e){const{_viewDim1:t,_viewDim2:i}=this;Object.assign(this._viewportSize,e),i!==this._viewDim2?this._viewDim2Changed():t!==this._viewDim1&&this._checkThresholds()}get viewportScroll(){return this._latestCoords}set viewportScroll(e){Object.assign(this._latestCoords,e);const t=this._scrollPosition;this._scrollPosition=this._latestCoords[this._positionDim],t!==this._scrollPosition&&(this._scrollPositionChanged(t,this._scrollPosition),this._updateVisibleIndices({emit:!0})),this._checkThresholds()}reflowIfNeeded(e){(e||this._pendingReflow)&&(this._pendingReflow=!1,this._reflow())}scrollToIndex(e,t="start"){if(Number.isFinite(e)){switch(e=Math.min(this.totalItems,Math.max(0,e)),this._scrollToIndex=e,"nearest"===t&&(t=e>this._first+this._num/2?"end":"start"),t){case"start":this._scrollToAnchor=0;break;case"center":this._scrollToAnchor=.5;break;case"end":this._scrollToAnchor=1;break;default:throw new TypeError("position must be one of: start, center, end, nearest")}this._scheduleReflow()}}async dispatchEvent(...e){await this._eventTargetPromise,this._eventTarget.dispatchEvent(...e)}async addEventListener(...e){await this._eventTargetPromise,this._eventTarget.addEventListener(...e)}async removeEventListener(...e){await this._eventTargetPromise,this._eventTarget.removeEventListener(...e)}_itemDim2Changed(){}_viewDim2Changed(){}_updateLayout(){}_getItemSize(e){return{[this._sizeDim]:this._itemDim1,[this._secondarySizeDim]:this._itemDim2}}get _delta(){return this._itemDim1+this._spacing}get _itemDim1(){return this._itemSize[this._sizeDim]}get _itemDim2(){return this._itemSize[this._secondarySizeDim]}get _viewDim1(){return this._viewportSize[this._sizeDim]}get _viewDim2(){return this._viewportSize[this._secondarySizeDim]}_scheduleReflow(){this._pendingReflow=!0}_scheduleLayoutUpdate(){this._pendingLayoutUpdate=!0,this._scheduleReflow()}_reflow(){const{_first:e,_last:t,_scrollSize:i}=this;this._pendingLayoutUpdate&&(this._updateLayout(),this._pendingLayoutUpdate=!1),this._updateScrollSize(),this._getActiveItems(),this._scrollIfNeeded(),this._updateVisibleIndices(),this._scrollSize!==i&&this._emitScrollSize(),-1===this._first&&-1===this._last?this._emitRange():(this._first!==e||this._last!==t||this._spacingChanged)&&(this._emitRange(),this._emitChildPositions()),this._emitScrollError()}_updateScrollSize(){this._scrollSize=Math.max(1,this._totalItems*this._delta)}_scrollIfNeeded(){if(-1===this._scrollToIndex)return;const e=this._scrollToIndex,t=this._scrollToAnchor,i=this._getItemPosition(e)[this._positionDim],n=this._getItemSize(e)[this._sizeDim],o=this._scrollPosition+this._viewDim1*t,s=i+n*t,a=Math.floor(Math.min(this._scrollSize-this._viewDim1,Math.max(0,this._scrollPosition-o+s)));this._scrollError+=this._scrollPosition-a,this._scrollPosition=a}_emitRange(e){const t=Object.assign({first:this._first,last:this._last,num:this._num,stable:!0,firstVisible:this._firstVisible,lastVisible:this._lastVisible},e);this.dispatchEvent(new CustomEvent("rangechange",{detail:t}))}_emitScrollSize(){const e={[this._sizeDim]:this._scrollSize};this.dispatchEvent(new CustomEvent("scrollsizechange",{detail:e}))}_emitScrollError(){if(this._scrollError){const e={[this._positionDim]:this._scrollError,[this._secondaryPositionDim]:0};this.dispatchEvent(new CustomEvent("scrollerrorchange",{detail:e})),this._scrollError=0}}_emitChildPositions(){const e={};for(let t=this._first;t<=this._last;t++)e[t]=this._getItemPosition(t);this.dispatchEvent(new CustomEvent("itempositionchange",{detail:e}))}get _num(){return-1===this._first||-1===this._last?0:this._last-this._first+1}_checkThresholds(){if(0===this._viewDim1&&this._num>0)this._scheduleReflow();else{const e=Math.max(0,this._scrollPosition-this._overhang),t=Math.min(this._scrollSize,this._scrollPosition+this._viewDim1+this._overhang);(this._physicalMin>e||this._physicalMax<t)&&this._scheduleReflow()}}_updateVisibleIndices(e){if(-1===this._first||-1===this._last)return;let t=this._first;for(;Math.round(this._getItemPosition(t)[this._positionDim]+this._getItemSize(t)[this._sizeDim])<=Math.round(this._scrollPosition);)t++;let i=this._last;for(;Math.round(this._getItemPosition(i)[this._positionDim])>=Math.round(this._scrollPosition+this._viewDim1);)i--;t===this._firstVisible&&i===this._lastVisible||(this._firstVisible=t,this._lastVisible=i,e&&e.emit&&this._emitRange())}_scrollPositionChanged(e,t){const i=this._scrollSize-this._viewDim1;(e<i||t<i)&&(this._scrollToIndex=-1)}}Ae._defaultConfig={};class Re extends Ae{constructor(e){super(e),this._physicalItems=new Map,this._newPhysicalItems=new Map,this._metrics=new Map,this._anchorIdx=null,this._anchorPos=null,this._stable=!0,this._needsRemeasure=!1,this._nMeasured=0,this._tMeasured=0,this._measureChildren=!0,this._estimate=!0}get measureChildren(){return this._measureChildren}updateItemSizes(e){Object.keys(e).forEach(t=>{const i=e[t],n=this._getMetrics(Number(t)),o=n[this._sizeDim];n.width=i.width+(i.marginLeft||0)+(i.marginRight||0),n.height=i.height+(i.marginTop||0)+(i.marginBottom||0);const s=n[this._sizeDim],a=this._getPhysicalItem(Number(t));if(a){let e;void 0!==s&&(a.size=s,void 0===o?(e=s,this._nMeasured++):e=s-o),this._tMeasured=this._tMeasured+e}}),this._nMeasured&&(this._updateItemSize(),this._scheduleReflow())}_updateItemSize(){this._itemSize[this._sizeDim]=Math.round(this._tMeasured/this._nMeasured)}_getMetrics(e){return this._metrics[e]=this._metrics[e]||{}}_getPhysicalItem(e){return this._newPhysicalItems.get(e)||this._physicalItems.get(e)}_getSize(e){const t=this._getPhysicalItem(e);return t&&t.size}_getPosition(e){const t=this._getPhysicalItem(e);return t?t.pos:e*this._delta+this._spacing}_calculateAnchor(e,t){return 0===e?0:t>this._scrollSize-this._viewDim1?this._totalItems-1:Math.max(0,Math.min(this._totalItems-1,Math.floor((e+t)/2/this._delta)))}_getAnchor(e,t){if(0===this._physicalItems.size)return this._calculateAnchor(e,t);if(this._first<0)return console.error("_getAnchor: negative _first"),this._calculateAnchor(e,t);if(this._last<0)return console.error("_getAnchor: negative _last"),this._calculateAnchor(e,t);const i=this._getPhysicalItem(this._first),n=this._getPhysicalItem(this._last),o=i.pos,s=o+i.size,a=n.pos,r=a+n.size;if(r<e)return this._calculateAnchor(e,t);if(o>t)return this._calculateAnchor(e,t);if(o>=e||s>=e)return this._first;if(r<=t||a<=t)return this._last;let c=this._last,l=this._first;for(;;){const i=Math.round((c+l)/2),n=this._physicalItems.get(i),o=n.pos,s=o+n.size;if(o>=e&&o<=t||s>=e&&s<=t)return i;s<e?l=i+1:o>t&&(c=i-1)}}_getActiveItems(){0===this._viewDim1||0===this._totalItems?this._clearItems():this._getItems()}_clearItems(){this._first=-1,this._last=-1,this._physicalMin=0,this._physicalMax=0;const e=this._newPhysicalItems;this._newPhysicalItems=this._physicalItems,this._newPhysicalItems.clear(),this._physicalItems=e,this._stable=!0}_getItems(){const e=this._newPhysicalItems;let t,i;this._scrollToIndex>=0?(this._anchorIdx=this._scrollToIndex,this._anchorPos=this._getPosition(this._anchorIdx),this._scrollIfNeeded(),t=Math.max(0,this._scrollPosition-this._overhang),i=Math.min(this._scrollSize,this._scrollPosition+this._viewDim1+this._overhang)):(i=Math.min(this._scrollSize,this._scrollPosition+this._viewDim1+this._overhang),t=Math.max(0,i-this._viewDim1-2*this._overhang),null!==this._anchorIdx&&null!==this._anchorPos||(this._anchorIdx=this._getAnchor(t,i),this._anchorPos=this._getPosition(this._anchorIdx)));let n=this._getSize(this._anchorIdx);void 0===n&&(n=this._itemDim1);let o=0;for(this._anchorPos+n+this._spacing<t&&(o=t-(this._anchorPos+n+this._spacing)),this._anchorPos>i&&(o=i-this._anchorPos),o&&(this._scrollPosition-=o,t-=o,i-=o,this._scrollError+=o),e.set(this._anchorIdx,{pos:this._anchorPos,size:n}),this._first=this._last=this._anchorIdx,this._physicalMin=this._physicalMax=this._anchorPos,this._stable=!0;this._physicalMin>t&&this._first>0;){let t=this._getSize(--this._first);void 0===t&&(this._stable=!1,t=this._itemDim1);const i=this._physicalMin-=t+this._spacing;if(e.set(this._first,{pos:i,size:t}),!1===this._stable&&!1===this._estimate)break}for(;this._physicalMax<i&&this._last<this._totalItems;){let t=this._getSize(this._last);if(void 0===t&&(this._stable=!1,t=this._itemDim1),e.set(this._last++,{pos:this._physicalMax,size:t}),!1===this._stable&&!1===this._estimate)break;this._physicalMax+=t+this._spacing}this._last--;const s=this._calculateError();s&&(this._physicalMin-=s,this._physicalMax-=s,this._anchorPos-=s,this._scrollPosition-=s,e.forEach(e=>e.pos-=s),this._scrollError+=s),this._stable&&(this._newPhysicalItems=this._physicalItems,this._newPhysicalItems.clear(),this._physicalItems=e)}_calculateError(){return 0===this._first?this._physicalMin:this._physicalMin<=0?this._physicalMin-this._first*this._delta:this._last===this._totalItems-1?this._physicalMax-this._scrollSize:this._physicalMax>=this._scrollSize?this._physicalMax-this._scrollSize+(this._totalItems-1-this._last)*this._delta:0}_updateScrollSize(){super._updateScrollSize(),this._scrollSize=Math.max(this._physicalMax,this._scrollSize)}_reflow(){const{_first:e,_last:t,_scrollSize:i}=this;this._updateScrollSize(),this._getActiveItems(),this._scrollSize!==i&&this._emitScrollSize(),this._updateVisibleIndices(),this._emitRange(),-1===this._first&&-1===this._last?this._resetReflowState():this._first!==e||this._last!==t||this._needsRemeasure?(this._emitChildPositions(),this._emitScrollError()):(this._emitChildPositions(),this._emitScrollError(),this._resetReflowState())}_resetReflowState(){this._anchorIdx=null,this._anchorPos=null,this._stable=!0}_getItemPosition(e){return{[this._positionDim]:this._getPosition(e),[this._secondaryPositionDim]:0}}_getItemSize(e){return{[this._sizeDim]:this._getSize(e)||this._itemDim1,[this._secondarySizeDim]:this._itemDim2}}_viewDim2Changed(){this._needsRemeasure=!0,this._scheduleReflow()}_emitRange(){const e=this._needsRemeasure,t=this._stable;this._needsRemeasure=!1,super._emitRange({remeasure:e,stable:t})}}function Oe(e,t,i,n){var o,s=arguments.length,a=s<3?t:null===n?n=Object.getOwnPropertyDescriptor(t,i):n;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)a=Reflect.decorate(e,t,i,n);else for(var r=e.length-1;r>=0;r--)(o=e[r])&&(a=(s<3?o(a):s>3?o(t,i,a):o(t,i))||a);return s>3&&a&&Object.defineProperty(t,i,a),a}let Fe=class extends r{constructor(){super(...arguments),this.scrollTarget=this}createRenderRoot(){return this}set layout(e){this._layout=e,this.requestUpdate()}get layout(){return this[ge].layout}async scrollToIndex(e,t="start"){this._scrollToIndex={index:e,position:t},this.requestUpdate(),await this.updateComplete,this._scrollToIndex=null}render(){const{items:e,renderItem:t,keyFunction:i,scrollTarget:n}=this,o=this._layout;return l`
            ${Ie({items:e,renderItem:t,layout:o,keyFunction:i,scrollTarget:n,scrollToIndex:this._scrollToIndex})}
        `}};function ze(e){if(!e||"object"!=typeof e)return e;if("[object Date]"==Object.prototype.toString.call(e))return new Date(e.getTime());if(Array.isArray(e))return e.map(ze);var t={};return Object.keys(e).forEach((function(i){t[i]=ze(e[i])})),t}Oe([s()],Fe.prototype,"renderItem",void 0),Oe([s({attribute:!1})],Fe.prototype,"items",void 0),Oe([s({attribute:!1})],Fe.prototype,"scrollTarget",void 0),Oe([s()],Fe.prototype,"keyFunction",void 0),Oe([s({attribute:!1})],Fe.prototype,"layout",null),Fe=Oe([p("lit-virtualizer")],Fe);const Me=e=>t=>({kind:"method",placement:"prototype",key:t.key,descriptor:{set(e){this["__"+String(t.key)]=e},get(){return this["__"+String(t.key)]},enumerable:!0,configurable:!0},finisher(i){const n=i.prototype.connectedCallback;i.prototype.connectedCallback=function(){if(n.call(this),this[t.key]){const i=this.renderRoot.querySelector(e);if(!i)return;i.scrollTop=this[t.key]}}}}),Le=v({_template:y`
    <style>
      :host {
        display: inline-block;
        position: fixed;
        clip: rect(0px,0px,0px,0px);
      }
    </style>
    <div aria-live$="[[mode]]">[[_text]]</div>
`,is:"iron-a11y-announcer",properties:{mode:{type:String,value:"polite"},timeout:{type:Number,value:150},_text:{type:String,value:""}},created:function(){Le.instance||(Le.instance=this),document.addEventListener("iron-announce",this._onIronAnnounce.bind(this))},announce:function(e){this._text="",this.async((function(){this._text=e}),this.timeout)},_onIronAnnounce:function(e){e.detail&&e.detail.text&&this.announce(e.detail.text)}});Le.instance=null,Le.requestAvailability=function(){Le.instance||(Le.instance=document.createElement("iron-a11y-announcer")),document.body?document.body.appendChild(Le.instance):document.addEventListener("load",(function(){document.body.appendChild(Le.instance)}))};class De{constructor(e){De[" "](e),this.type=e&&e.type||"default",this.key=e&&e.key,e&&"value"in e&&(this.value=e.value)}get value(){var e=this.type,t=this.key;if(e&&t)return De.types[e]&&De.types[e][t]}set value(e){var t=this.type,i=this.key;t&&i&&(t=De.types[t]=De.types[t]||{},null==e?delete t[i]:t[i]=e)}get list(){if(this.type){var e=De.types[this.type];return e?Object.keys(e).map((function(e){return Be[this.type][e]}),this):[]}}byKey(e){return this.key=e,this.value}}De[" "]=function(){},De.types={};var Be=De.types;v({is:"iron-meta",properties:{type:{type:String,value:"default"},key:{type:String},value:{type:String,notify:!0},self:{type:Boolean,observer:"_selfChanged"},__meta:{type:Boolean,computed:"__computeMeta(type, key, value)"}},hostAttributes:{hidden:!0},__computeMeta:function(e,t,i){var n=new De({type:e,key:t});return void 0!==i&&i!==n.value?n.value=i:this.value!==n.value&&(this.value=n.value),n},get list(){return this.__meta&&this.__meta.list},_selfChanged:function(e){e&&(this.value=this)},byKey:function(e){return new De({type:this.type,key:e}).value}});let $e=null;const Pe={properties:{validator:{type:String},invalid:{notify:!0,reflectToAttribute:!0,type:Boolean,value:!1,observer:"_invalidChanged"}},registered:function(){$e=new De({type:"validator"})},_invalidChanged:function(){this.invalid?this.setAttribute("aria-invalid","true"):this.removeAttribute("aria-invalid")},get _validator(){return $e&&$e.byKey(this.validator)},hasValidator:function(){return null!=this._validator},validate:function(e){return void 0===e&&void 0!==this.value?this.invalid=!this._getValidity(this.value):this.invalid=!this._getValidity(e),!this.invalid},_getValidity:function(e){return!this.hasValidator()||this._validator.validate(e)}};v({_template:y`
    <style>
      :host {
        display: inline-block;
      }
    </style>
    <slot id="content"></slot>
`,is:"iron-input",behaviors:[Pe],properties:{bindValue:{type:String,value:""},value:{type:String,computed:"_computeValue(bindValue)"},allowedPattern:{type:String},autoValidate:{type:Boolean,value:!1},_inputElement:Object},observers:["_bindValueChanged(bindValue, _inputElement)"],listeners:{input:"_onInput",keypress:"_onKeypress"},created:function(){Le.requestAvailability(),this._previousValidInput="",this._patternAlreadyChecked=!1},attached:function(){this._observer=x(this).observeNodes(function(e){this._initSlottedInput()}.bind(this))},detached:function(){this._observer&&(x(this).unobserveNodes(this._observer),this._observer=null)},get inputElement(){return this._inputElement},_initSlottedInput:function(){this._inputElement=this.getEffectiveChildren()[0],this.inputElement&&this.inputElement.value&&(this.bindValue=this.inputElement.value),this.fire("iron-input-ready")},get _patternRegExp(){var e;if(this.allowedPattern)e=new RegExp(this.allowedPattern);else switch(this.inputElement.type){case"number":e=/[0-9.,e-]/}return e},_bindValueChanged:function(e,t){t&&(void 0===e?t.value=null:e!==t.value&&(this.inputElement.value=e),this.autoValidate&&this.validate(),this.fire("bind-value-changed",{value:e}))},_onInput:function(){this.allowedPattern&&!this._patternAlreadyChecked&&(this._checkPatternValidity()||(this._announceInvalidCharacter("Invalid string of characters not entered."),this.inputElement.value=this._previousValidInput));this.bindValue=this._previousValidInput=this.inputElement.value,this._patternAlreadyChecked=!1},_isPrintable:function(e){var t=8==e.keyCode||9==e.keyCode||13==e.keyCode||27==e.keyCode,i=19==e.keyCode||20==e.keyCode||45==e.keyCode||46==e.keyCode||144==e.keyCode||145==e.keyCode||e.keyCode>32&&e.keyCode<41||e.keyCode>111&&e.keyCode<124;return!(t||0==e.charCode&&i)},_onKeypress:function(e){if(this.allowedPattern||"number"===this.inputElement.type){var t=this._patternRegExp;if(t&&!(e.metaKey||e.ctrlKey||e.altKey)){this._patternAlreadyChecked=!0;var i=String.fromCharCode(e.charCode);this._isPrintable(e)&&!t.test(i)&&(e.preventDefault(),this._announceInvalidCharacter("Invalid character "+i+" not entered."))}}},_checkPatternValidity:function(){var e=this._patternRegExp;if(!e)return!0;for(var t=0;t<this.inputElement.value.length;t++)if(!e.test(this.inputElement.value[t]))return!1;return!0},validate:function(){if(!this.inputElement)return this.invalid=!1,!0;var e=this.inputElement.checkValidity();return e&&(this.required&&""===this.bindValue?e=!1:this.hasValidator()&&(e=Pe.validate.call(this,this.bindValue))),this.invalid=!e,this.fire("iron-input-validate"),e},_announceInvalidCharacter:function(e){this.fire("iron-announce",{text:e})},_computeValue:function(e){return e}});const Ne={attached:function(){this.fire("addon-attached")},update:function(e){}};v({_template:y`
    <style>
      :host {
        display: inline-block;
        float: right;

        @apply --paper-font-caption;
        @apply --paper-input-char-counter;
      }

      :host([hidden]) {
        display: none !important;
      }

      :host(:dir(rtl)) {
        float: left;
      }
    </style>

    <span>[[_charCounterStr]]</span>
`,is:"paper-input-char-counter",behaviors:[Ne],properties:{_charCounterStr:{type:String,value:"0"}},update:function(e){if(e.inputElement){e.value=e.value||"";var t=e.value.toString().length.toString();e.inputElement.hasAttribute("maxlength")&&(t+="/"+e.inputElement.getAttribute("maxlength")),this._charCounterStr=t}}});const He=y`
<custom-style>
  <style is="custom-style">
    html {
      --paper-input-container-shared-input-style: {
        position: relative; /* to make a stacking context */
        outline: none;
        box-shadow: none;
        padding: 0;
        margin: 0;
        width: 100%;
        max-width: 100%;
        background: transparent;
        border: none;
        color: var(--paper-input-container-input-color, var(--primary-text-color));
        -webkit-appearance: none;
        text-align: inherit;
        vertical-align: var(--paper-input-container-input-align, bottom);

        @apply --paper-font-subhead;
      };
    }
  </style>
</custom-style>
`;He.setAttribute("style","display: none;"),document.head.appendChild(He.content),v({_template:y`
    <style>
      :host {
        display: block;
        padding: 8px 0;
        @apply --paper-input-container;
      }

      :host([inline]) {
        display: inline-block;
      }

      :host([disabled]) {
        pointer-events: none;
        opacity: 0.33;

        @apply --paper-input-container-disabled;
      }

      :host([hidden]) {
        display: none !important;
      }

      [hidden] {
        display: none !important;
      }

      .floated-label-placeholder {
        @apply --paper-font-caption;
      }

      .underline {
        height: 2px;
        position: relative;
      }

      .focused-line {
        @apply --layout-fit;
        border-bottom: 2px solid var(--paper-input-container-focus-color, var(--primary-color));

        -webkit-transform-origin: center center;
        transform-origin: center center;
        -webkit-transform: scale3d(0,1,1);
        transform: scale3d(0,1,1);

        @apply --paper-input-container-underline-focus;
      }

      .underline.is-highlighted .focused-line {
        -webkit-transform: none;
        transform: none;
        -webkit-transition: -webkit-transform 0.25s;
        transition: transform 0.25s;

        @apply --paper-transition-easing;
      }

      .underline.is-invalid .focused-line {
        border-color: var(--paper-input-container-invalid-color, var(--error-color));
        -webkit-transform: none;
        transform: none;
        -webkit-transition: -webkit-transform 0.25s;
        transition: transform 0.25s;

        @apply --paper-transition-easing;
      }

      .unfocused-line {
        @apply --layout-fit;
        border-bottom: 1px solid var(--paper-input-container-color, var(--secondary-text-color));
        @apply --paper-input-container-underline;
      }

      :host([disabled]) .unfocused-line {
        border-bottom: 1px dashed;
        border-color: var(--paper-input-container-color, var(--secondary-text-color));
        @apply --paper-input-container-underline-disabled;
      }

      .input-wrapper {
        @apply --layout-horizontal;
        @apply --layout-center;
        position: relative;
      }

      .input-content {
        @apply --layout-flex-auto;
        @apply --layout-relative;
        max-width: 100%;
      }

      .input-content ::slotted(label),
      .input-content ::slotted(.paper-input-label) {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        font: inherit;
        color: var(--paper-input-container-color, var(--secondary-text-color));
        -webkit-transition: -webkit-transform 0.25s, width 0.25s;
        transition: transform 0.25s, width 0.25s;
        -webkit-transform-origin: left top;
        transform-origin: left top;
        /* Fix for safari not focusing 0-height date/time inputs with -webkit-apperance: none; */
        min-height: 1px;

        @apply --paper-font-common-nowrap;
        @apply --paper-font-subhead;
        @apply --paper-input-container-label;
        @apply --paper-transition-easing;
      }


      .input-content ::slotted(label):before,
      .input-content ::slotted(.paper-input-label):before {
        @apply --paper-input-container-label-before;
      }

      .input-content ::slotted(label):after,
      .input-content ::slotted(.paper-input-label):after {
        @apply --paper-input-container-label-after;
      }

      .input-content.label-is-floating ::slotted(label),
      .input-content.label-is-floating ::slotted(.paper-input-label) {
        -webkit-transform: translateY(-75%) scale(0.75);
        transform: translateY(-75%) scale(0.75);

        /* Since we scale to 75/100 of the size, we actually have 100/75 of the
        original space now available */
        width: 133%;

        @apply --paper-input-container-label-floating;
      }

      :host(:dir(rtl)) .input-content.label-is-floating ::slotted(label),
      :host(:dir(rtl)) .input-content.label-is-floating ::slotted(.paper-input-label) {
        right: 0;
        left: auto;
        -webkit-transform-origin: right top;
        transform-origin: right top;
      }

      .input-content.label-is-highlighted ::slotted(label),
      .input-content.label-is-highlighted ::slotted(.paper-input-label) {
        color: var(--paper-input-container-focus-color, var(--primary-color));

        @apply --paper-input-container-label-focus;
      }

      .input-content.is-invalid ::slotted(label),
      .input-content.is-invalid ::slotted(.paper-input-label) {
        color: var(--paper-input-container-invalid-color, var(--error-color));
      }

      .input-content.label-is-hidden ::slotted(label),
      .input-content.label-is-hidden ::slotted(.paper-input-label) {
        visibility: hidden;
      }

      .input-content ::slotted(input),
      .input-content ::slotted(iron-input),
      .input-content ::slotted(textarea),
      .input-content ::slotted(iron-autogrow-textarea),
      .input-content ::slotted(.paper-input-input) {
        @apply --paper-input-container-shared-input-style;
        /* The apply shim doesn't apply the nested color custom property,
          so we have to re-apply it here. */
        color: var(--paper-input-container-input-color, var(--primary-text-color));
        @apply --paper-input-container-input;
      }

      .input-content ::slotted(input)::-webkit-outer-spin-button,
      .input-content ::slotted(input)::-webkit-inner-spin-button {
        @apply --paper-input-container-input-webkit-spinner;
      }

      .input-content.focused ::slotted(input),
      .input-content.focused ::slotted(iron-input),
      .input-content.focused ::slotted(textarea),
      .input-content.focused ::slotted(iron-autogrow-textarea),
      .input-content.focused ::slotted(.paper-input-input) {
        @apply --paper-input-container-input-focus;
      }

      .input-content.is-invalid ::slotted(input),
      .input-content.is-invalid ::slotted(iron-input),
      .input-content.is-invalid ::slotted(textarea),
      .input-content.is-invalid ::slotted(iron-autogrow-textarea),
      .input-content.is-invalid ::slotted(.paper-input-input) {
        @apply --paper-input-container-input-invalid;
      }

      .prefix ::slotted(*) {
        display: inline-block;
        @apply --paper-font-subhead;
        @apply --layout-flex-none;
        @apply --paper-input-prefix;
      }

      .suffix ::slotted(*) {
        display: inline-block;
        @apply --paper-font-subhead;
        @apply --layout-flex-none;

        @apply --paper-input-suffix;
      }

      /* Firefox sets a min-width on the input, which can cause layout issues */
      .input-content ::slotted(input) {
        min-width: 0;
      }

      .input-content ::slotted(textarea) {
        resize: none;
      }

      .add-on-content {
        position: relative;
      }

      .add-on-content.is-invalid ::slotted(*) {
        color: var(--paper-input-container-invalid-color, var(--error-color));
      }

      .add-on-content.is-highlighted ::slotted(*) {
        color: var(--paper-input-container-focus-color, var(--primary-color));
      }
    </style>

    <div class="floated-label-placeholder" aria-hidden="true" hidden="[[noLabelFloat]]">&nbsp;</div>

    <div class="input-wrapper">
      <span class="prefix"><slot name="prefix"></slot></span>

      <div class$="[[_computeInputContentClass(noLabelFloat,alwaysFloatLabel,focused,invalid,_inputHasContent)]]" id="labelAndInputContainer">
        <slot name="label"></slot>
        <slot name="input"></slot>
      </div>

      <span class="suffix"><slot name="suffix"></slot></span>
    </div>

    <div class$="[[_computeUnderlineClass(focused,invalid)]]">
      <div class="unfocused-line"></div>
      <div class="focused-line"></div>
    </div>

    <div class$="[[_computeAddOnContentClass(focused,invalid)]]">
      <slot name="add-on"></slot>
    </div>
`,is:"paper-input-container",properties:{noLabelFloat:{type:Boolean,value:!1},alwaysFloatLabel:{type:Boolean,value:!1},attrForValue:{type:String,value:"bind-value"},autoValidate:{type:Boolean,value:!1},invalid:{observer:"_invalidChanged",type:Boolean,value:!1},focused:{readOnly:!0,type:Boolean,value:!1,notify:!0},_addons:{type:Array},_inputHasContent:{type:Boolean,value:!1},_inputSelector:{type:String,value:"input,iron-input,textarea,.paper-input-input"},_boundOnFocus:{type:Function,value:function(){return this._onFocus.bind(this)}},_boundOnBlur:{type:Function,value:function(){return this._onBlur.bind(this)}},_boundOnInput:{type:Function,value:function(){return this._onInput.bind(this)}},_boundValueChanged:{type:Function,value:function(){return this._onValueChanged.bind(this)}}},listeners:{"addon-attached":"_onAddonAttached","iron-input-validate":"_onIronInputValidate"},get _valueChangedEvent(){return this.attrForValue+"-changed"},get _propertyForValue(){return k(this.attrForValue)},get _inputElement(){return x(this).querySelector(this._inputSelector)},get _inputElementValue(){return this._inputElement[this._propertyForValue]||this._inputElement.value},ready:function(){this.__isFirstValueUpdate=!0,this._addons||(this._addons=[]),this.addEventListener("focus",this._boundOnFocus,!0),this.addEventListener("blur",this._boundOnBlur,!0)},attached:function(){this.attrForValue?this._inputElement.addEventListener(this._valueChangedEvent,this._boundValueChanged):this.addEventListener("input",this._onInput),this._inputElementValue&&""!=this._inputElementValue?this._handleValueAndAutoValidate(this._inputElement):this._handleValue(this._inputElement)},_onAddonAttached:function(e){this._addons||(this._addons=[]);var t=e.target;-1===this._addons.indexOf(t)&&(this._addons.push(t),this.isAttached&&this._handleValue(this._inputElement))},_onFocus:function(){this._setFocused(!0)},_onBlur:function(){this._setFocused(!1),this._handleValueAndAutoValidate(this._inputElement)},_onInput:function(e){this._handleValueAndAutoValidate(e.target)},_onValueChanged:function(e){var t=e.target;this.__isFirstValueUpdate&&(this.__isFirstValueUpdate=!1,void 0===t.value||""===t.value)||this._handleValueAndAutoValidate(e.target)},_handleValue:function(e){var t=this._inputElementValue;t||0===t||"number"===e.type&&!e.checkValidity()?this._inputHasContent=!0:this._inputHasContent=!1,this.updateAddons({inputElement:e,value:t,invalid:this.invalid})},_handleValueAndAutoValidate:function(e){var t;this.autoValidate&&e&&(t=e.validate?e.validate(this._inputElementValue):e.checkValidity(),this.invalid=!t);this._handleValue(e)},_onIronInputValidate:function(e){this.invalid=this._inputElement.invalid},_invalidChanged:function(){this._addons&&this.updateAddons({invalid:this.invalid})},updateAddons:function(e){for(var t,i=0;t=this._addons[i];i++)t.update(e)},_computeInputContentClass:function(e,t,i,n,o){var s="input-content";if(e)o&&(s+=" label-is-hidden"),n&&(s+=" is-invalid");else{var a=this.querySelector("label");t||o?(s+=" label-is-floating",this.$.labelAndInputContainer.style.position="static",n?s+=" is-invalid":i&&(s+=" label-is-highlighted")):(a&&(this.$.labelAndInputContainer.style.position="relative"),n&&(s+=" is-invalid"))}return i&&(s+=" focused"),s},_computeUnderlineClass:function(e,t){var i="underline";return t?i+=" is-invalid":e&&(i+=" is-highlighted"),i},_computeAddOnContentClass:function(e,t){var i="add-on-content";return t?i+=" is-invalid":e&&(i+=" is-highlighted"),i}}),v({_template:y`
    <style>
      :host {
        display: inline-block;
        visibility: hidden;

        color: var(--paper-input-container-invalid-color, var(--error-color));

        @apply --paper-font-caption;
        @apply --paper-input-error;
        position: absolute;
        left:0;
        right:0;
      }

      :host([invalid]) {
        visibility: visible;
      }

      #a11yWrapper {
        visibility: hidden;
      }

      :host([invalid]) #a11yWrapper {
        visibility: visible;
      }
    </style>

    <!--
    If the paper-input-error element is directly referenced by an
    \`aria-describedby\` attribute, such as when used as a paper-input add-on,
    then applying \`visibility: hidden;\` to the paper-input-error element itself
    does not hide the error.

    For more information, see:
    https://www.w3.org/TR/accname-1.1/#mapping_additional_nd_description
    -->
    <div id="a11yWrapper">
      <slot></slot>
    </div>
`,is:"paper-input-error",behaviors:[Ne],properties:{invalid:{readOnly:!0,reflectToAttribute:!0,type:Boolean}},update:function(e){this._setInvalid(e.invalid)}});const Ve={properties:{name:{type:String},value:{notify:!0,type:String},required:{type:Boolean,value:!1}},attached:function(){},detached:function(){}};var Ue={"U+0008":"backspace","U+0009":"tab","U+001B":"esc","U+0020":"space","U+007F":"del"},Ke={8:"backspace",9:"tab",13:"enter",27:"esc",33:"pageup",34:"pagedown",35:"end",36:"home",32:"space",37:"left",38:"up",39:"right",40:"down",46:"del",106:"*"},We={shift:"shiftKey",ctrl:"ctrlKey",alt:"altKey",meta:"metaKey"},Ge=/[a-z0-9*]/,je=/U\+/,qe=/^arrow/,Xe=/^space(bar)?/,Qe=/^escape$/;function Ye(e,t){var i="";if(e){var n=e.toLowerCase();" "===n||Xe.test(n)?i="space":Qe.test(n)?i="esc":1==n.length?t&&!Ge.test(n)||(i=n):i=qe.test(n)?n.replace("arrow",""):"multiply"==n?"*":n}return i}function Ze(e,t){return e.key?Ye(e.key,t):e.detail&&e.detail.key?Ye(e.detail.key,t):(i=e.keyIdentifier,n="",i&&(i in Ue?n=Ue[i]:je.test(i)?(i=parseInt(i.replace("U+","0x"),16),n=String.fromCharCode(i).toLowerCase()):n=i.toLowerCase()),n||function(e){var t="";return Number(e)&&(t=e>=65&&e<=90?String.fromCharCode(32+e):e>=112&&e<=123?"f"+(e-112+1):e>=48&&e<=57?String(e-48):e>=96&&e<=105?String(e-96):Ke[e]),t}(e.keyCode)||"");var i,n}function Je(e,t){return Ze(t,e.hasModifiers)===e.key&&(!e.hasModifiers||!!t.shiftKey==!!e.shiftKey&&!!t.ctrlKey==!!e.ctrlKey&&!!t.altKey==!!e.altKey&&!!t.metaKey==!!e.metaKey)}function et(e){return e.trim().split(" ").map((function(e){return function(e){return 1===e.length?{combo:e,key:e,event:"keydown"}:e.split("+").reduce((function(e,t){var i=t.split(":"),n=i[0],o=i[1];return n in We?(e[We[n]]=!0,e.hasModifiers=!0):(e.key=n,e.event=o||"keydown"),e}),{combo:e.split(":").shift()})}(e)}))}const tt={properties:{keyEventTarget:{type:Object,value:function(){return this}},stopKeyboardEventPropagation:{type:Boolean,value:!1},_boundKeyHandlers:{type:Array,value:function(){return[]}},_imperativeKeyBindings:{type:Object,value:function(){return{}}}},observers:["_resetKeyEventListeners(keyEventTarget, _boundKeyHandlers)"],keyBindings:{},registered:function(){this._prepKeyBindings()},attached:function(){this._listenKeyEventListeners()},detached:function(){this._unlistenKeyEventListeners()},addOwnKeyBinding:function(e,t){this._imperativeKeyBindings[e]=t,this._prepKeyBindings(),this._resetKeyEventListeners()},removeOwnKeyBindings:function(){this._imperativeKeyBindings={},this._prepKeyBindings(),this._resetKeyEventListeners()},keyboardEventMatchesKeys:function(e,t){for(var i=et(t),n=0;n<i.length;++n)if(Je(i[n],e))return!0;return!1},_collectKeyBindings:function(){var e=this.behaviors.map((function(e){return e.keyBindings}));return-1===e.indexOf(this.keyBindings)&&e.push(this.keyBindings),e},_prepKeyBindings:function(){for(var e in this._keyBindings={},this._collectKeyBindings().forEach((function(e){for(var t in e)this._addKeyBinding(t,e[t])}),this),this._imperativeKeyBindings)this._addKeyBinding(e,this._imperativeKeyBindings[e]);for(var t in this._keyBindings)this._keyBindings[t].sort((function(e,t){var i=e[0].hasModifiers;return i===t[0].hasModifiers?0:i?-1:1}))},_addKeyBinding:function(e,t){et(e).forEach((function(e){this._keyBindings[e.event]=this._keyBindings[e.event]||[],this._keyBindings[e.event].push([e,t])}),this)},_resetKeyEventListeners:function(){this._unlistenKeyEventListeners(),this.isAttached&&this._listenKeyEventListeners()},_listenKeyEventListeners:function(){this.keyEventTarget&&Object.keys(this._keyBindings).forEach((function(e){var t=this._keyBindings[e],i=this._onKeyBindingEvent.bind(this,t);this._boundKeyHandlers.push([this.keyEventTarget,e,i]),this.keyEventTarget.addEventListener(e,i)}),this)},_unlistenKeyEventListeners:function(){for(var e,t,i,n;this._boundKeyHandlers.length;)t=(e=this._boundKeyHandlers.pop())[0],i=e[1],n=e[2],t.removeEventListener(i,n)},_onKeyBindingEvent:function(e,t){if(this.stopKeyboardEventPropagation&&t.stopPropagation(),!t.defaultPrevented)for(var i=0;i<e.length;i++){var n=e[i][0],o=e[i][1];if(Je(n,t)&&(this._triggerKeyHandler(n,o,t),t.defaultPrevented))return}},_triggerKeyHandler:function(e,t,i){var n=Object.create(e);n.keyboardEvent=i;var o=new CustomEvent(e.event,{detail:n,cancelable:!0});this[t].call(this,o),o.defaultPrevented&&i.preventDefault()}},it={properties:{focused:{type:Boolean,value:!1,notify:!0,readOnly:!0,reflectToAttribute:!0},disabled:{type:Boolean,value:!1,notify:!0,observer:"_disabledChanged",reflectToAttribute:!0},_oldTabIndex:{type:String},_boundFocusBlurHandler:{type:Function,value:function(){return this._focusBlurHandler.bind(this)}}},observers:["_changedControlState(focused, disabled)"],ready:function(){this.addEventListener("focus",this._boundFocusBlurHandler,!0),this.addEventListener("blur",this._boundFocusBlurHandler,!0)},_focusBlurHandler:function(e){this._setFocused("focus"===e.type)},_disabledChanged:function(e,t){this.setAttribute("aria-disabled",e?"true":"false"),this.style.pointerEvents=e?"none":"",e?(this._oldTabIndex=this.getAttribute("tabindex"),this._setFocused(!1),this.tabIndex=-1,this.blur()):void 0!==this._oldTabIndex&&(null===this._oldTabIndex?this.removeAttribute("tabindex"):this.setAttribute("tabindex",this._oldTabIndex))},_changedControlState:function(){this._controlStateChanged&&this._controlStateChanged()}},nt={NextLabelID:1,NextAddonID:1,NextInputID:1},ot={properties:{label:{type:String},value:{notify:!0,type:String},disabled:{type:Boolean,value:!1},invalid:{type:Boolean,value:!1,notify:!0},allowedPattern:{type:String},type:{type:String},list:{type:String},pattern:{type:String},required:{type:Boolean,value:!1},errorMessage:{type:String},charCounter:{type:Boolean,value:!1},noLabelFloat:{type:Boolean,value:!1},alwaysFloatLabel:{type:Boolean,value:!1},autoValidate:{type:Boolean,value:!1},validator:{type:String},autocomplete:{type:String,value:"off"},autofocus:{type:Boolean,observer:"_autofocusChanged"},inputmode:{type:String},minlength:{type:Number},maxlength:{type:Number},min:{type:String},max:{type:String},step:{type:String},name:{type:String},placeholder:{type:String,value:""},readonly:{type:Boolean,value:!1},size:{type:Number},autocapitalize:{type:String,value:"none"},autocorrect:{type:String,value:"off"},autosave:{type:String},results:{type:Number},accept:{type:String},multiple:{type:Boolean},_ariaDescribedBy:{type:String,value:""},_ariaLabelledBy:{type:String,value:""},_inputId:{type:String,value:""}},listeners:{"addon-attached":"_onAddonAttached"},keyBindings:{"shift+tab:keydown":"_onShiftTabDown"},hostAttributes:{tabindex:0},get inputElement(){return this.$||(this.$={}),this.$.input||(this._generateInputId(),this.$.input=this.$$("#"+this._inputId)),this.$.input},get _focusableElement(){return this.inputElement},created:function(){this._typesThatHaveText=["date","datetime","datetime-local","month","time","week","file"]},attached:function(){this._updateAriaLabelledBy(),!w&&this.inputElement&&-1!==this._typesThatHaveText.indexOf(this.inputElement.type)&&(this.alwaysFloatLabel=!0)},_appendStringWithSpace:function(e,t){return e=e?e+" "+t:t},_onAddonAttached:function(e){var t=x(e).rootTarget;if(t.id)this._ariaDescribedBy=this._appendStringWithSpace(this._ariaDescribedBy,t.id);else{var i="paper-input-add-on-"+nt.NextAddonID++;t.id=i,this._ariaDescribedBy=this._appendStringWithSpace(this._ariaDescribedBy,i)}},validate:function(){return this.inputElement.validate()},_focusBlurHandler:function(e){it._focusBlurHandler.call(this,e),this.focused&&!this._shiftTabPressed&&this._focusableElement&&this._focusableElement.focus()},_onShiftTabDown:function(e){var t=this.getAttribute("tabindex");this._shiftTabPressed=!0,this.setAttribute("tabindex","-1"),this.async((function(){this.setAttribute("tabindex",t),this._shiftTabPressed=!1}),1)},_handleAutoValidate:function(){this.autoValidate&&this.validate()},updateValueAndPreserveCaret:function(e){try{var t=this.inputElement.selectionStart;this.value=e,this.inputElement.selectionStart=t,this.inputElement.selectionEnd=t}catch(t){this.value=e}},_computeAlwaysFloatLabel:function(e,t){return t||e},_updateAriaLabelledBy:function(){var e,t=x(this.root).querySelector("label");t?(t.id?e=t.id:(e="paper-input-label-"+nt.NextLabelID++,t.id=e),this._ariaLabelledBy=e):this._ariaLabelledBy=""},_generateInputId:function(){this._inputId&&""!==this._inputId||(this._inputId="input-"+nt.NextInputID++)},_onChange:function(e){this.shadowRoot&&this.fire(e.type,{sourceEvent:e},{node:this,bubbles:e.bubbles,cancelable:e.cancelable})},_autofocusChanged:function(){if(this.autofocus&&this._focusableElement){var e=document.activeElement;e instanceof HTMLElement&&e!==document.body&&e!==document.documentElement||this._focusableElement.focus()}}},st=[it,tt,ot];v({is:"paper-input",_template:y`
    <style>
      :host {
        display: block;
      }

      :host([focused]) {
        outline: none;
      }

      :host([hidden]) {
        display: none !important;
      }

      input {
        /* Firefox sets a min-width on the input, which can cause layout issues */
        min-width: 0;
      }

      /* In 1.x, the <input> is distributed to paper-input-container, which styles it.
      In 2.x the <iron-input> is distributed to paper-input-container, which styles
      it, but in order for this to work correctly, we need to reset some
      of the native input's properties to inherit (from the iron-input) */
      iron-input > input {
        @apply --paper-input-container-shared-input-style;
        font-family: inherit;
        font-weight: inherit;
        font-size: inherit;
        letter-spacing: inherit;
        word-spacing: inherit;
        line-height: inherit;
        text-shadow: inherit;
        color: inherit;
        cursor: inherit;
      }

      input:disabled {
        @apply --paper-input-container-input-disabled;
      }

      input::-webkit-outer-spin-button,
      input::-webkit-inner-spin-button {
        @apply --paper-input-container-input-webkit-spinner;
      }

      input::-webkit-clear-button {
        @apply --paper-input-container-input-webkit-clear;
      }

      input::-webkit-calendar-picker-indicator {
        @apply --paper-input-container-input-webkit-calendar-picker-indicator;
      }

      input::-webkit-input-placeholder {
        color: var(--paper-input-container-color, var(--secondary-text-color));
      }

      input:-moz-placeholder {
        color: var(--paper-input-container-color, var(--secondary-text-color));
      }

      input::-moz-placeholder {
        color: var(--paper-input-container-color, var(--secondary-text-color));
      }

      input::-ms-clear {
        @apply --paper-input-container-ms-clear;
      }

      input::-ms-reveal {
        @apply --paper-input-container-ms-reveal;
      }

      input:-ms-input-placeholder {
        color: var(--paper-input-container-color, var(--secondary-text-color));
      }

      label {
        pointer-events: none;
      }
    </style>

    <paper-input-container id="container" no-label-float="[[noLabelFloat]]" always-float-label="[[_computeAlwaysFloatLabel(alwaysFloatLabel,placeholder)]]" auto-validate$="[[autoValidate]]" disabled$="[[disabled]]" invalid="[[invalid]]">

      <slot name="prefix" slot="prefix"></slot>

      <label hidden$="[[!label]]" aria-hidden="true" for$="[[_inputId]]" slot="label">[[label]]</label>

      <!-- Need to bind maxlength so that the paper-input-char-counter works correctly -->
      <iron-input bind-value="{{value}}" slot="input" class="input-element" id$="[[_inputId]]" maxlength$="[[maxlength]]" allowed-pattern="[[allowedPattern]]" invalid="{{invalid}}" validator="[[validator]]">
        <input aria-labelledby$="[[_ariaLabelledBy]]" aria-describedby$="[[_ariaDescribedBy]]" disabled$="[[disabled]]" title$="[[title]]" type$="[[type]]" pattern$="[[pattern]]" required$="[[required]]" autocomplete$="[[autocomplete]]" autofocus$="[[autofocus]]" inputmode$="[[inputmode]]" minlength$="[[minlength]]" maxlength$="[[maxlength]]" min$="[[min]]" max$="[[max]]" step$="[[step]]" name$="[[name]]" placeholder$="[[placeholder]]" readonly$="[[readonly]]" list$="[[list]]" size$="[[size]]" autocapitalize$="[[autocapitalize]]" autocorrect$="[[autocorrect]]" on-change="_onChange" tabindex$="[[tabIndex]]" autosave$="[[autosave]]" results$="[[results]]" accept$="[[accept]]" multiple$="[[multiple]]" role$="[[inputRole]]" aria-haspopup$="[[inputAriaHaspopup]]">
      </iron-input>

      <slot name="suffix" slot="suffix"></slot>

      <template is="dom-if" if="[[errorMessage]]">
        <paper-input-error aria-live="assertive" slot="add-on">[[errorMessage]]</paper-input-error>
      </template>

      <template is="dom-if" if="[[charCounter]]">
        <paper-input-char-counter slot="add-on"></paper-input-char-counter>
      </template>

    </paper-input-container>
  `,behaviors:[st,Ve],properties:{value:{type:String},inputRole:{type:String,value:void 0},inputAriaHaspopup:{type:String,value:void 0}},get _focusableElement(){return this.inputElement._inputElement},listeners:{"iron-input-ready":"_onIronInputReady"},_onIronInputReady:function(){this.$.nativeInput||(this.$.nativeInput=this.$$("input")),this.inputElement&&-1!==this._typesThatHaveText.indexOf(this.$.nativeInput.type)&&(this.alwaysFloatLabel=!0),this.inputElement.bindValue&&this.$.container._handleValueAndAutoValidate(this.inputElement)}}),E([p("search-input")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[s({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s()],key:"filter",value:void 0},{kind:"field",decorators:[s({type:Boolean,attribute:"no-label-float"})],key:"noLabelFloat",value:()=>!1},{kind:"field",decorators:[s({type:Boolean,attribute:"no-underline"})],key:"noUnderline",value:()=>!1},{kind:"field",decorators:[s({type:Boolean})],key:"autofocus",value:()=>!1},{kind:"field",decorators:[s({type:String})],key:"label",value:void 0},{kind:"method",key:"focus",value:function(){this.shadowRoot.querySelector("paper-input").focus()}},{kind:"field",decorators:[n("paper-input",!0)],key:"_input",value:void 0},{kind:"method",key:"render",value:function(){return l`
      <paper-input
        .autofocus=${this.autofocus}
        .label=${this.label||"Search"}
        .value=${this.filter}
        @value-changed=${this._filterInputChanged}
        .noLabelFloat=${this.noLabelFloat}
      >
        <slot name="prefix" slot="prefix">
          <ha-svg-icon class="prefix" .path=${I}></ha-svg-icon>
        </slot>
        ${this.filter&&l`
          <ha-icon-button
            slot="suffix"
            @click=${this._clearSearch}
            .label=${this.hass.localize("ui.common.clear")}
            .path=${C}
          ></ha-icon-button>
        `}
      </paper-input>
    `}},{kind:"method",key:"updated",value:function(e){e.has("noUnderline")&&(this.noUnderline||void 0!==e.get("noUnderline"))&&(this._input.inputElement.parentElement.shadowRoot.querySelector("div.unfocused-line").style.display=this.noUnderline?"none":"block")}},{kind:"method",key:"_filterChanged",value:async function(e){S(this,"value-changed",{value:String(e)})}},{kind:"method",key:"_filterInputChanged",value:async function(e){this._filterChanged(e.target.value)}},{kind:"method",key:"_clearSearch",value:async function(){this._filterChanged("")}},{kind:"get",static:!0,key:"styles",value:function(){return h`
      ha-svg-icon,
      ha-icon-button {
        color: var(--primary-text-color);
      }
      ha-icon-button {
        --mdc-icon-button-size: 24px;
      }
      ha-svg-icon.prefix {
        margin: 8px;
      }
    `}}]}}),r);const at=(e,t,i=!1)=>{let n;return(...o)=>{const s=i&&!n;clearTimeout(n),n=window.setTimeout(()=>{n=void 0,i||e(...o)},t),s&&e(...o)}},rt=()=>new Promise(e=>{var t;t=e,requestAnimationFrame(()=>setTimeout(t,0))});var ct,lt;const dt=null!==(lt=null===(ct=window.ShadyDOM)||void 0===ct?void 0:ct.inUse)&&void 0!==lt&&lt;class ht extends T{constructor(){super(...arguments),this.disabled=!1,this.containingForm=null,this.formDataListener=e=>{this.disabled||this.setFormData(e.formData)}}findFormElement(){if(!this.shadowRoot||dt)return null;const e=this.getRootNode().querySelectorAll("form");for(const t of Array.from(e))if(t.contains(this))return t;return null}connectedCallback(){var e;super.connectedCallback(),this.containingForm=this.findFormElement(),null===(e=this.containingForm)||void 0===e||e.addEventListener("formdata",this.formDataListener)}disconnectedCallback(){var e;super.disconnectedCallback(),null===(e=this.containingForm)||void 0===e||e.removeEventListener("formdata",this.formDataListener),this.containingForm=null}click(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}firstUpdated(){super.firstUpdated(),this.shadowRoot&&this.mdcRoot.addEventListener("change",e=>{this.dispatchEvent(new Event("change",e))})}}ht.shadowRootOptions={mode:"open",delegatesFocus:!0},i([s({type:Boolean})],ht.prototype,"disabled",void 0);class pt extends ht{constructor(){super(...arguments),this.checked=!1,this.indeterminate=!1,this.disabled=!1,this.name="",this.value="on",this.reducedTouchTarget=!1,this.animationClass="",this.shouldRenderRipple=!1,this.focused=!1,this.mdcFoundationClass=void 0,this.mdcFoundation=void 0,this.rippleElement=null,this.rippleHandlers=new c(()=>(this.shouldRenderRipple=!0,this.ripple.then(e=>this.rippleElement=e),this.ripple))}createAdapter(){return{}}update(e){const t=e.get("indeterminate"),i=e.get("checked"),n=e.get("disabled");if(void 0!==t||void 0!==i||void 0!==n){const e=this.calculateAnimationStateName(!!i,!!t,!!n),o=this.calculateAnimationStateName(this.checked,this.indeterminate,this.disabled);this.animationClass=`${e}-${o}`}super.update(e)}calculateAnimationStateName(e,t,i){return i?"disabled":t?"indeterminate":e?"checked":"unchecked"}renderRipple(){return this.shouldRenderRipple?this.renderRippleTemplate():""}renderRippleTemplate(){return l`<mwc-ripple
        .disabled="${this.disabled}"
        unbounded></mwc-ripple>`}render(){const e=this.indeterminate||this.checked,t={"mdc-checkbox--disabled":this.disabled,"mdc-checkbox--selected":e,"mdc-checkbox--touch":!this.reducedTouchTarget,"mdc-ripple-upgraded--background-focused":this.focused,"mdc-checkbox--anim-checked-indeterminate":"checked-indeterminate"==this.animationClass,"mdc-checkbox--anim-checked-unchecked":"checked-unchecked"==this.animationClass,"mdc-checkbox--anim-indeterminate-checked":"indeterminate-checked"==this.animationClass,"mdc-checkbox--anim-indeterminate-unchecked":"indeterminate-unchecked"==this.animationClass,"mdc-checkbox--anim-unchecked-checked":"unchecked-checked"==this.animationClass,"mdc-checkbox--anim-unchecked-indeterminate":"unchecked-indeterminate"==this.animationClass},i=this.indeterminate?"mixed":void 0;return l`
      <div class="mdc-checkbox mdc-checkbox--upgraded ${d(t)}">
        <input type="checkbox"
              class="mdc-checkbox__native-control"
              name="${O(this.name)}"
              aria-checked="${O(i)}"
              aria-label="${O(this.ariaLabel)}"
              aria-labelledby="${O(this.ariaLabelledBy)}"
              aria-describedby="${O(this.ariaDescribedBy)}"
              data-indeterminate="${this.indeterminate?"true":"false"}"
              ?disabled="${this.disabled}"
              .indeterminate="${this.indeterminate}"
              .checked="${this.checked}"
              .value="${this.value}"
              @change="${this.handleChange}"
              @focus="${this.handleFocus}"
              @blur="${this.handleBlur}"
              @mousedown="${this.handleRippleMouseDown}"
              @mouseenter="${this.handleRippleMouseEnter}"
              @mouseleave="${this.handleRippleMouseLeave}"
              @touchstart="${this.handleRippleTouchStart}"
              @touchend="${this.handleRippleDeactivate}"
              @touchcancel="${this.handleRippleDeactivate}">
        <div class="mdc-checkbox__background"
          @animationend="${this.resetAnimationClass}">
          <svg class="mdc-checkbox__checkmark"
              viewBox="0 0 24 24">
            <path class="mdc-checkbox__checkmark-path"
                  fill="none"
                  d="M1.73,12.91 8.1,19.28 22.79,4.59"></path>
          </svg>
          <div class="mdc-checkbox__mixedmark"></div>
        </div>
        ${this.renderRipple()}
      </div>`}setFormData(e){this.name&&this.checked&&e.append(this.name,this.value)}handleFocus(){this.focused=!0,this.handleRippleFocus()}handleBlur(){this.focused=!1,this.handleRippleBlur()}handleRippleMouseDown(e){const t=()=>{window.removeEventListener("mouseup",t),this.handleRippleDeactivate()};window.addEventListener("mouseup",t),this.rippleHandlers.startPress(e)}handleRippleTouchStart(e){this.rippleHandlers.startPress(e)}handleRippleDeactivate(){this.rippleHandlers.endPress()}handleRippleMouseEnter(){this.rippleHandlers.startHover()}handleRippleMouseLeave(){this.rippleHandlers.endHover()}handleRippleFocus(){this.rippleHandlers.startFocus()}handleRippleBlur(){this.rippleHandlers.endFocus()}handleChange(){this.checked=this.formElement.checked,this.indeterminate=this.formElement.indeterminate}resetAnimationClass(){this.animationClass=""}get isRippleActive(){var e;return(null===(e=this.rippleElement)||void 0===e?void 0:e.isActive)||!1}}i([n(".mdc-checkbox")],pt.prototype,"mdcRoot",void 0),i([n("input")],pt.prototype,"formElement",void 0),i([s({type:Boolean,reflect:!0})],pt.prototype,"checked",void 0),i([s({type:Boolean})],pt.prototype,"indeterminate",void 0),i([s({type:Boolean,reflect:!0})],pt.prototype,"disabled",void 0),i([s({type:String,reflect:!0})],pt.prototype,"name",void 0),i([s({type:String})],pt.prototype,"value",void 0),i([A,s({type:String,attribute:"aria-label"})],pt.prototype,"ariaLabel",void 0),i([A,s({type:String,attribute:"aria-labelledby"})],pt.prototype,"ariaLabelledBy",void 0),i([A,s({type:String,attribute:"aria-describedby"})],pt.prototype,"ariaDescribedBy",void 0),i([s({type:Boolean})],pt.prototype,"reducedTouchTarget",void 0),i([a()],pt.prototype,"animationClass",void 0),i([a()],pt.prototype,"shouldRenderRipple",void 0),i([a()],pt.prototype,"focused",void 0),i([o("mwc-ripple")],pt.prototype,"ripple",void 0),i([R({passive:!0})],pt.prototype,"handleRippleTouchStart",null);const ut=h`.mdc-checkbox{padding:calc((40px - 18px) / 2);padding:calc((var(--mdc-checkbox-ripple-size, 40px) - 18px) / 2);margin:calc((40px - 40px) / 2);margin:calc((var(--mdc-checkbox-touch-target-size, 40px) - 40px) / 2)}.mdc-checkbox .mdc-checkbox__ripple::before,.mdc-checkbox .mdc-checkbox__ripple::after{background-color:#000;background-color:var(--mdc-ripple-color, #000)}.mdc-checkbox:hover .mdc-checkbox__ripple::before,.mdc-checkbox.mdc-ripple-surface--hover .mdc-checkbox__ripple::before{opacity:0.04;opacity:var(--mdc-ripple-hover-opacity, 0.04)}.mdc-checkbox.mdc-ripple-upgraded--background-focused .mdc-checkbox__ripple::before,.mdc-checkbox:not(.mdc-ripple-upgraded):focus .mdc-checkbox__ripple::before{transition-duration:75ms;opacity:0.12;opacity:var(--mdc-ripple-focus-opacity, 0.12)}.mdc-checkbox:not(.mdc-ripple-upgraded) .mdc-checkbox__ripple::after{transition:opacity 150ms linear}.mdc-checkbox:not(.mdc-ripple-upgraded):active .mdc-checkbox__ripple::after{transition-duration:75ms;opacity:0.12;opacity:var(--mdc-ripple-press-opacity, 0.12)}.mdc-checkbox.mdc-ripple-upgraded{--mdc-ripple-fg-opacity:var(--mdc-ripple-press-opacity, 0.12)}.mdc-checkbox.mdc-checkbox--selected .mdc-checkbox__ripple::before,.mdc-checkbox.mdc-checkbox--selected .mdc-checkbox__ripple::after{background-color:#018786;background-color:var(--mdc-ripple-color, var(--mdc-theme-secondary, #018786))}.mdc-checkbox.mdc-checkbox--selected:hover .mdc-checkbox__ripple::before,.mdc-checkbox.mdc-checkbox--selected.mdc-ripple-surface--hover .mdc-checkbox__ripple::before{opacity:0.04;opacity:var(--mdc-ripple-hover-opacity, 0.04)}.mdc-checkbox.mdc-checkbox--selected.mdc-ripple-upgraded--background-focused .mdc-checkbox__ripple::before,.mdc-checkbox.mdc-checkbox--selected:not(.mdc-ripple-upgraded):focus .mdc-checkbox__ripple::before{transition-duration:75ms;opacity:0.12;opacity:var(--mdc-ripple-focus-opacity, 0.12)}.mdc-checkbox.mdc-checkbox--selected:not(.mdc-ripple-upgraded) .mdc-checkbox__ripple::after{transition:opacity 150ms linear}.mdc-checkbox.mdc-checkbox--selected:not(.mdc-ripple-upgraded):active .mdc-checkbox__ripple::after{transition-duration:75ms;opacity:0.12;opacity:var(--mdc-ripple-press-opacity, 0.12)}.mdc-checkbox.mdc-checkbox--selected.mdc-ripple-upgraded{--mdc-ripple-fg-opacity:var(--mdc-ripple-press-opacity, 0.12)}.mdc-checkbox.mdc-ripple-upgraded--background-focused.mdc-checkbox--selected .mdc-checkbox__ripple::before,.mdc-checkbox.mdc-ripple-upgraded--background-focused.mdc-checkbox--selected .mdc-checkbox__ripple::after{background-color:#018786;background-color:var(--mdc-ripple-color, var(--mdc-theme-secondary, #018786))}.mdc-checkbox .mdc-checkbox__background{top:calc((40px - 18px) / 2);top:calc((var(--mdc-checkbox-ripple-size, 40px) - 18px) / 2);left:calc((40px - 18px) / 2);left:calc((var(--mdc-checkbox-ripple-size, 40px) - 18px) / 2)}.mdc-checkbox .mdc-checkbox__native-control{top:calc((40px - 40px) / 2);top:calc((40px - var(--mdc-checkbox-touch-target-size, 40px)) / 2);right:calc((40px - 40px) / 2);right:calc((40px - var(--mdc-checkbox-touch-target-size, 40px)) / 2);left:calc((40px - 40px) / 2);left:calc((40px - var(--mdc-checkbox-touch-target-size, 40px)) / 2);width:40px;width:var(--mdc-checkbox-touch-target-size, 40px);height:40px;height:var(--mdc-checkbox-touch-target-size, 40px)}.mdc-checkbox .mdc-checkbox__native-control:enabled:not(:checked):not(:indeterminate):not([data-indeterminate=true])~.mdc-checkbox__background{border-color:rgba(0, 0, 0, 0.54);border-color:var(--mdc-checkbox-unchecked-color, rgba(0, 0, 0, 0.54));background-color:transparent}.mdc-checkbox .mdc-checkbox__native-control:enabled:checked~.mdc-checkbox__background,.mdc-checkbox .mdc-checkbox__native-control:enabled:indeterminate~.mdc-checkbox__background,.mdc-checkbox .mdc-checkbox__native-control[data-indeterminate=true]:enabled~.mdc-checkbox__background{border-color:#018786;border-color:var(--mdc-checkbox-checked-color, var(--mdc-theme-secondary, #018786));background-color:#018786;background-color:var(--mdc-checkbox-checked-color, var(--mdc-theme-secondary, #018786))}@keyframes mdc-checkbox-fade-in-background-8A000000FF01878600000000FF018786{0%{border-color:rgba(0, 0, 0, 0.54);border-color:var(--mdc-checkbox-unchecked-color, rgba(0, 0, 0, 0.54));background-color:transparent}50%{border-color:#018786;border-color:var(--mdc-checkbox-checked-color, var(--mdc-theme-secondary, #018786));background-color:#018786;background-color:var(--mdc-checkbox-checked-color, var(--mdc-theme-secondary, #018786))}}@keyframes mdc-checkbox-fade-out-background-8A000000FF01878600000000FF018786{0%,80%{border-color:#018786;border-color:var(--mdc-checkbox-checked-color, var(--mdc-theme-secondary, #018786));background-color:#018786;background-color:var(--mdc-checkbox-checked-color, var(--mdc-theme-secondary, #018786))}100%{border-color:rgba(0, 0, 0, 0.54);border-color:var(--mdc-checkbox-unchecked-color, rgba(0, 0, 0, 0.54));background-color:transparent}}.mdc-checkbox.mdc-checkbox--anim-unchecked-checked .mdc-checkbox__native-control:enabled~.mdc-checkbox__background,.mdc-checkbox.mdc-checkbox--anim-unchecked-indeterminate .mdc-checkbox__native-control:enabled~.mdc-checkbox__background{animation-name:mdc-checkbox-fade-in-background-8A000000FF01878600000000FF018786}.mdc-checkbox.mdc-checkbox--anim-checked-unchecked .mdc-checkbox__native-control:enabled~.mdc-checkbox__background,.mdc-checkbox.mdc-checkbox--anim-indeterminate-unchecked .mdc-checkbox__native-control:enabled~.mdc-checkbox__background{animation-name:mdc-checkbox-fade-out-background-8A000000FF01878600000000FF018786}.mdc-checkbox .mdc-checkbox__native-control[disabled]:not(:checked):not(:indeterminate):not([data-indeterminate=true])~.mdc-checkbox__background{border-color:rgba(0, 0, 0, 0.38);border-color:var(--mdc-checkbox-disabled-color, rgba(0, 0, 0, 0.38));background-color:transparent}.mdc-checkbox .mdc-checkbox__native-control[disabled]:checked~.mdc-checkbox__background,.mdc-checkbox .mdc-checkbox__native-control[disabled]:indeterminate~.mdc-checkbox__background,.mdc-checkbox .mdc-checkbox__native-control[data-indeterminate=true][disabled]~.mdc-checkbox__background{border-color:transparent;background-color:rgba(0, 0, 0, 0.38);background-color:var(--mdc-checkbox-disabled-color, rgba(0, 0, 0, 0.38))}.mdc-checkbox .mdc-checkbox__native-control:enabled~.mdc-checkbox__background .mdc-checkbox__checkmark{color:#fff;color:var(--mdc-checkbox-ink-color, #fff)}.mdc-checkbox .mdc-checkbox__native-control:enabled~.mdc-checkbox__background .mdc-checkbox__mixedmark{border-color:#fff;border-color:var(--mdc-checkbox-ink-color, #fff)}.mdc-checkbox .mdc-checkbox__native-control:disabled~.mdc-checkbox__background .mdc-checkbox__checkmark{color:#fff;color:var(--mdc-checkbox-ink-color, #fff)}.mdc-checkbox .mdc-checkbox__native-control:disabled~.mdc-checkbox__background .mdc-checkbox__mixedmark{border-color:#fff;border-color:var(--mdc-checkbox-ink-color, #fff)}.mdc-touch-target-wrapper{display:inline}@keyframes mdc-checkbox-unchecked-checked-checkmark-path{0%,50%{stroke-dashoffset:29.7833385}50%{animation-timing-function:cubic-bezier(0, 0, 0.2, 1)}100%{stroke-dashoffset:0}}@keyframes mdc-checkbox-unchecked-indeterminate-mixedmark{0%,68.2%{transform:scaleX(0)}68.2%{animation-timing-function:cubic-bezier(0, 0, 0, 1)}100%{transform:scaleX(1)}}@keyframes mdc-checkbox-checked-unchecked-checkmark-path{from{animation-timing-function:cubic-bezier(0.4, 0, 1, 1);opacity:1;stroke-dashoffset:0}to{opacity:0;stroke-dashoffset:-29.7833385}}@keyframes mdc-checkbox-checked-indeterminate-checkmark{from{animation-timing-function:cubic-bezier(0, 0, 0.2, 1);transform:rotate(0deg);opacity:1}to{transform:rotate(45deg);opacity:0}}@keyframes mdc-checkbox-indeterminate-checked-checkmark{from{animation-timing-function:cubic-bezier(0.14, 0, 0, 1);transform:rotate(45deg);opacity:0}to{transform:rotate(360deg);opacity:1}}@keyframes mdc-checkbox-checked-indeterminate-mixedmark{from{animation-timing-function:mdc-animation-deceleration-curve-timing-function;transform:rotate(-45deg);opacity:0}to{transform:rotate(0deg);opacity:1}}@keyframes mdc-checkbox-indeterminate-checked-mixedmark{from{animation-timing-function:cubic-bezier(0.14, 0, 0, 1);transform:rotate(0deg);opacity:1}to{transform:rotate(315deg);opacity:0}}@keyframes mdc-checkbox-indeterminate-unchecked-mixedmark{0%{animation-timing-function:linear;transform:scaleX(1);opacity:1}32.8%,100%{transform:scaleX(0);opacity:0}}.mdc-checkbox{display:inline-block;position:relative;flex:0 0 18px;box-sizing:content-box;width:18px;height:18px;line-height:0;white-space:nowrap;cursor:pointer;vertical-align:bottom}@media screen and (forced-colors: active),(-ms-high-contrast: active){.mdc-checkbox__native-control[disabled]:not(:checked):not(:indeterminate):not([data-indeterminate=true])~.mdc-checkbox__background{border-color:GrayText;border-color:var(--mdc-checkbox-disabled-color, GrayText);background-color:transparent}.mdc-checkbox__native-control[disabled]:checked~.mdc-checkbox__background,.mdc-checkbox__native-control[disabled]:indeterminate~.mdc-checkbox__background,.mdc-checkbox__native-control[data-indeterminate=true][disabled]~.mdc-checkbox__background{border-color:GrayText;background-color:transparent;background-color:var(--mdc-checkbox-disabled-color, transparent)}.mdc-checkbox__native-control:disabled~.mdc-checkbox__background .mdc-checkbox__checkmark{color:GrayText;color:var(--mdc-checkbox-ink-color, GrayText)}.mdc-checkbox__native-control:disabled~.mdc-checkbox__background .mdc-checkbox__mixedmark{border-color:GrayText;border-color:var(--mdc-checkbox-ink-color, GrayText)}.mdc-checkbox__mixedmark{margin:0 1px}}.mdc-checkbox--disabled{cursor:default;pointer-events:none}.mdc-checkbox__background{display:inline-flex;position:absolute;align-items:center;justify-content:center;box-sizing:border-box;width:18px;height:18px;border:2px solid currentColor;border-radius:2px;background-color:transparent;pointer-events:none;will-change:background-color,border-color;transition:background-color 90ms 0ms cubic-bezier(0.4, 0, 0.6, 1),border-color 90ms 0ms cubic-bezier(0.4, 0, 0.6, 1)}.mdc-checkbox__checkmark{position:absolute;top:0;right:0;bottom:0;left:0;width:100%;opacity:0;transition:opacity 180ms 0ms cubic-bezier(0.4, 0, 0.6, 1)}.mdc-checkbox--upgraded .mdc-checkbox__checkmark{opacity:1}.mdc-checkbox__checkmark-path{transition:stroke-dashoffset 180ms 0ms cubic-bezier(0.4, 0, 0.6, 1);stroke:currentColor;stroke-width:3.12px;stroke-dashoffset:29.7833385;stroke-dasharray:29.7833385}.mdc-checkbox__mixedmark{width:100%;height:0;transform:scaleX(0) rotate(0deg);border-width:1px;border-style:solid;opacity:0;transition:opacity 90ms 0ms cubic-bezier(0.4, 0, 0.6, 1),transform 90ms 0ms cubic-bezier(0.4, 0, 0.6, 1)}.mdc-checkbox--anim-unchecked-checked .mdc-checkbox__background,.mdc-checkbox--anim-unchecked-indeterminate .mdc-checkbox__background,.mdc-checkbox--anim-checked-unchecked .mdc-checkbox__background,.mdc-checkbox--anim-indeterminate-unchecked .mdc-checkbox__background{animation-duration:180ms;animation-timing-function:linear}.mdc-checkbox--anim-unchecked-checked .mdc-checkbox__checkmark-path{animation:mdc-checkbox-unchecked-checked-checkmark-path 180ms linear 0s;transition:none}.mdc-checkbox--anim-unchecked-indeterminate .mdc-checkbox__mixedmark{animation:mdc-checkbox-unchecked-indeterminate-mixedmark 90ms linear 0s;transition:none}.mdc-checkbox--anim-checked-unchecked .mdc-checkbox__checkmark-path{animation:mdc-checkbox-checked-unchecked-checkmark-path 90ms linear 0s;transition:none}.mdc-checkbox--anim-checked-indeterminate .mdc-checkbox__checkmark{animation:mdc-checkbox-checked-indeterminate-checkmark 90ms linear 0s;transition:none}.mdc-checkbox--anim-checked-indeterminate .mdc-checkbox__mixedmark{animation:mdc-checkbox-checked-indeterminate-mixedmark 90ms linear 0s;transition:none}.mdc-checkbox--anim-indeterminate-checked .mdc-checkbox__checkmark{animation:mdc-checkbox-indeterminate-checked-checkmark 500ms linear 0s;transition:none}.mdc-checkbox--anim-indeterminate-checked .mdc-checkbox__mixedmark{animation:mdc-checkbox-indeterminate-checked-mixedmark 500ms linear 0s;transition:none}.mdc-checkbox--anim-indeterminate-unchecked .mdc-checkbox__mixedmark{animation:mdc-checkbox-indeterminate-unchecked-mixedmark 300ms linear 0s;transition:none}.mdc-checkbox__native-control:checked~.mdc-checkbox__background,.mdc-checkbox__native-control:indeterminate~.mdc-checkbox__background,.mdc-checkbox__native-control[data-indeterminate=true]~.mdc-checkbox__background{transition:border-color 90ms 0ms cubic-bezier(0, 0, 0.2, 1),background-color 90ms 0ms cubic-bezier(0, 0, 0.2, 1)}.mdc-checkbox__native-control:checked~.mdc-checkbox__background .mdc-checkbox__checkmark-path,.mdc-checkbox__native-control:indeterminate~.mdc-checkbox__background .mdc-checkbox__checkmark-path,.mdc-checkbox__native-control[data-indeterminate=true]~.mdc-checkbox__background .mdc-checkbox__checkmark-path{stroke-dashoffset:0}.mdc-checkbox__native-control{position:absolute;margin:0;padding:0;opacity:0;cursor:inherit}.mdc-checkbox__native-control:disabled{cursor:default;pointer-events:none}.mdc-checkbox--touch{margin:calc((48px - 40px) / 2);margin:calc((var(--mdc-checkbox-state-layer-size, 48px) - var(--mdc-checkbox-state-layer-size, 40px)) / 2)}.mdc-checkbox--touch .mdc-checkbox__native-control{top:calc((40px - 48px) / 2);top:calc((var(--mdc-checkbox-state-layer-size, 40px) - var(--mdc-checkbox-state-layer-size, 48px)) / 2);right:calc((40px - 48px) / 2);right:calc((var(--mdc-checkbox-state-layer-size, 40px) - var(--mdc-checkbox-state-layer-size, 48px)) / 2);left:calc((40px - 48px) / 2);left:calc((var(--mdc-checkbox-state-layer-size, 40px) - var(--mdc-checkbox-state-layer-size, 48px)) / 2);width:48px;width:var(--mdc-checkbox-state-layer-size, 48px);height:48px;height:var(--mdc-checkbox-state-layer-size, 48px)}.mdc-checkbox__native-control:checked~.mdc-checkbox__background .mdc-checkbox__checkmark{transition:opacity 180ms 0ms cubic-bezier(0, 0, 0.2, 1),transform 180ms 0ms cubic-bezier(0, 0, 0.2, 1);opacity:1}.mdc-checkbox__native-control:checked~.mdc-checkbox__background .mdc-checkbox__mixedmark{transform:scaleX(1) rotate(-45deg)}.mdc-checkbox__native-control:indeterminate~.mdc-checkbox__background .mdc-checkbox__checkmark,.mdc-checkbox__native-control[data-indeterminate=true]~.mdc-checkbox__background .mdc-checkbox__checkmark{transform:rotate(45deg);opacity:0;transition:opacity 90ms 0ms cubic-bezier(0.4, 0, 0.6, 1),transform 90ms 0ms cubic-bezier(0.4, 0, 0.6, 1)}.mdc-checkbox__native-control:indeterminate~.mdc-checkbox__background .mdc-checkbox__mixedmark,.mdc-checkbox__native-control[data-indeterminate=true]~.mdc-checkbox__background .mdc-checkbox__mixedmark{transform:scaleX(1) rotate(0deg);opacity:1}.mdc-checkbox.mdc-checkbox--upgraded .mdc-checkbox__background,.mdc-checkbox.mdc-checkbox--upgraded .mdc-checkbox__checkmark,.mdc-checkbox.mdc-checkbox--upgraded .mdc-checkbox__checkmark-path,.mdc-checkbox.mdc-checkbox--upgraded .mdc-checkbox__mixedmark{transition:none}:host{outline:none;display:inline-flex;-webkit-tap-highlight-color:transparent}:host([checked]),:host([indeterminate]){--mdc-ripple-color:var(--mdc-theme-secondary, #018786)}.mdc-checkbox .mdc-checkbox__background::before{content:none}`;let mt=class extends pt{};mt.styles=[ut],mt=i([p("mwc-checkbox")],mt),E([p("ha-checkbox")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"method",key:"firstUpdated",value:function(){F(z(i.prototype),"firstUpdated",this).call(this),this.style.setProperty("--mdc-theme-secondary","var(--primary-color)")}}]}}),mt);E([p("insteon-data-table")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[s({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s({type:Object})],key:"columns",value:()=>({})},{kind:"field",decorators:[s({type:Array})],key:"data",value:()=>[]},{kind:"field",decorators:[s({type:Boolean})],key:"selectable",value:()=>!1},{kind:"field",decorators:[s({type:Boolean})],key:"clickable",value:()=>!1},{kind:"field",decorators:[s({type:Boolean})],key:"hasFab",value:()=>!1},{kind:"field",decorators:[s({attribute:!1})],key:"appendRow",value:void 0},{kind:"field",decorators:[s({type:Boolean,attribute:"auto-height"})],key:"autoHeight",value:()=>!1},{kind:"field",decorators:[s({type:String})],key:"id",value:()=>"id"},{kind:"field",decorators:[s({type:String})],key:"noDataText",value:void 0},{kind:"field",decorators:[s({type:String})],key:"searchLabel",value:void 0},{kind:"field",decorators:[s({type:Boolean,attribute:"no-label-float"})],key:"noLabelFloat",value:()=>!1},{kind:"field",decorators:[s({type:String})],key:"filter",value:()=>""},{kind:"field",decorators:[a()],key:"_filterable",value:()=>!1},{kind:"field",decorators:[a()],key:"_filter",value:()=>""},{kind:"field",decorators:[a()],key:"_sortColumn",value:void 0},{kind:"field",decorators:[a()],key:"_sortDirection",value:()=>null},{kind:"field",decorators:[a()],key:"_filteredData",value:()=>[]},{kind:"field",decorators:[a()],key:"_headerHeight",value:()=>0},{kind:"field",decorators:[n("slot[name='header']")],key:"_header",value:void 0},{kind:"field",decorators:[a()],key:"_items",value:()=>[]},{kind:"field",key:"_checkableRowsCount",value:void 0},{kind:"field",key:"_checkedRows",value:()=>[]},{kind:"field",key:"_sortColumns",value:()=>({})},{kind:"field",key:"curRequest",value:()=>0},{kind:"field",decorators:[Me(".scroller")],key:"_savedScrollPos",value:void 0},{kind:"field",key:"_debounceSearch",value(){return at(e=>{this._filter=e},100,!1)}},{kind:"method",key:"clearSelection",value:function(){this._checkedRows=[],this._checkedRowsChanged()}},{kind:"method",key:"connectedCallback",value:function(){F(z(i.prototype),"connectedCallback",this).call(this),this._items.length&&(this._items=[...this._items])}},{kind:"method",key:"firstUpdated",value:function(){this.updateComplete.then(()=>this._calcTableHeight())}},{kind:"method",key:"willUpdate",value:function(e){if(F(z(i.prototype),"willUpdate",this).call(this,e),e.has("columns")){this._filterable=Object.values(this.columns).some(e=>e.filterable);for(const e in this.columns)if(this.columns[e].direction){this._sortDirection=this.columns[e].direction,this._sortColumn=e;break}const e=ze(this.columns);Object.values(e).forEach(e=>{delete e.title,delete e.type,delete e.template}),this._sortColumns=e}e.has("filter")&&this._debounceSearch(this.filter),e.has("data")&&(this._checkableRowsCount=this.data.filter(e=>!1!==e.selectable).length),(e.has("data")||e.has("columns")||e.has("_filter")||e.has("_sortColumn")||e.has("_sortDirection"))&&this._sortFilterData()}},{kind:"method",key:"render",value:function(){return l`
      <div class="mdc-data-table">
        <slot name="header" @slotchange=${this._calcTableHeight}>
          ${this._filterable?l`
                <div class="table-header">
                  <search-input
                    .hass=${this.hass}
                    @value-changed=${this._handleSearchChange}
                    .label=${this.searchLabel}
                    .noLabelFloat=${this.noLabelFloat}
                  ></search-input>
                </div>
              `:""}
        </slot>
        <div
          class="mdc-data-table__table ${d({"auto-height":this.autoHeight})}"
          role="table"
          aria-rowcount=${this._filteredData.length-1}
          style=${M({height:this.autoHeight?53*(this._filteredData.length||1)+53+"px":`calc(100% - ${this._headerHeight}px)`})}
        >
          <div class="mdc-data-table__header-row" role="row" aria-rowindex="1">
            ${this.selectable?l`
                  <div
                    class="mdc-data-table__header-cell mdc-data-table__header-cell--checkbox"
                    role="columnheader"
                  >
                    <ha-checkbox
                      class="mdc-data-table__row-checkbox"
                      @change=${this._handleHeaderRowCheckboxClick}
                      .indeterminate=${this._checkedRows.length&&this._checkedRows.length!==this._checkableRowsCount}
                      .checked=${this._checkedRows.length===this._checkableRowsCount}
                    >
                    </ha-checkbox>
                  </div>
                `:""}
            ${Object.entries(this.columns).map(([e,t])=>{if(t.hidden)return"";const i=e===this._sortColumn,n={"mdc-data-table__header-cell--numeric":"numeric"===t.type,"mdc-data-table__header-cell--icon":"icon"===t.type,"mdc-data-table__header-cell--icon-button":"icon-button"===t.type,"mdc-data-table__header-cell--overflow-menu":"overflow-menu"===t.type,sortable:Boolean(t.sortable),"not-sorted":Boolean(t.sortable&&!i),grows:Boolean(t.grows)};return l`
                <div
                  class="mdc-data-table__header-cell ${d(n)}"
                  style=${t.width?M({[t.grows?"minWidth":"width"]:t.width,maxWidth:t.maxWidth||""}):""}
                  role="columnheader"
                  aria-sort=${O(i?"desc"===this._sortDirection?"descending":"ascending":void 0)}
                  @click=${this._handleHeaderClick}
                  .columnId=${e}
                >
                  ${t.sortable?l`
                        <ha-svg-icon
                          .path=${i&&"desc"===this._sortDirection?L:D}
                        ></ha-svg-icon>
                      `:""}
                  <span>${t.title}</span>
                </div>
              `})}
          </div>
          ${this._filteredData.length?l`
                <div
                  class="mdc-data-table__content scroller ha-scrollbar"
                  @scroll=${this._saveScrollPos}
                >
                  ${Ie({items:this._items,layout:Re,renderItem:(e,t)=>e?e.append?l` <div class="mdc-data-table__row">${e.content}</div> `:e.empty?l` <div class="mdc-data-table__row"></div> `:l`
                        <div
                          aria-rowindex=${t+2}
                          role="row"
                          .rowId=${e[this.id]}
                          @click=${this._handleRowClick}
                          class="mdc-data-table__row ${d({"mdc-data-table__row--selected":this._checkedRows.includes(String(e[this.id])),clickable:this.clickable})}"
                          aria-selected=${O(!!this._checkedRows.includes(String(e[this.id]))||void 0)}
                          .selectable=${!1!==e.selectable}
                        >
                          ${this.selectable?l`
                                <div
                                  class="mdc-data-table__cell mdc-data-table__cell--checkbox"
                                  role="cell"
                                >
                                  <ha-checkbox
                                    class="mdc-data-table__row-checkbox"
                                    @change=${this._handleRowCheckboxClick}
                                    .rowId=${e[this.id]}
                                    .disabled=${!1===e.selectable}
                                    .checked=${this._checkedRows.includes(String(e[this.id]))}
                                  >
                                  </ha-checkbox>
                                </div>
                              `:""}
                          ${Object.entries(this.columns).map(([t,i])=>i.hidden?"":l`
                              <div
                                role="cell"
                                class="mdc-data-table__cell ${d({"mdc-data-table__cell--numeric":"numeric"===i.type,"mdc-data-table__cell--icon":"icon"===i.type,"mdc-data-table__cell--icon-button":"icon-button"===i.type,"mdc-data-table__cell--overflow-menu":"overflow-menu"===i.type,grows:Boolean(i.grows),forceLTR:Boolean(i.forceLTR)})}"
                                style=${i.width?M({[i.grows?"minWidth":"width"]:i.width,maxWidth:i.maxWidth?i.maxWidth:""}):""}
                              >
                                ${i.template?i.template(e[t],e):e[t]}
                              </div>
                            `)}
                        </div>
                      `:l``})}
                </div>
              `:l`
                <div class="mdc-data-table__content">
                  <div class="mdc-data-table__row" role="row">
                    <div class="mdc-data-table__cell grows center" role="cell">
                      ${this.noDataText||"No data"}
                    </div>
                  </div>
                </div>
              `}
        </div>
      </div>
    `}},{kind:"method",key:"_sortFilterData",value:async function(){const e=(new Date).getTime();this.curRequest++;const t=this.curRequest;let i=this.data;this._filter&&(i=await this._memFilterData(this.data,this._sortColumns,this._filter));const n=this._sortColumn?((e,t,i,n)=>e.sort((e,o)=>{let s=1;"desc"===i&&(s=-1);let a=t.filterKey?e[t.valueColumn||n][t.filterKey]:e[t.valueColumn||n],r=t.filterKey?o[t.valueColumn||n][t.filterKey]:o[t.valueColumn||n];return"string"==typeof a&&(a=a.toUpperCase()),"string"==typeof r&&(r=r.toUpperCase()),void 0===a&&void 0!==r?1:void 0===r&&void 0!==a?-1:a<r?-1*s:a>r?1*s:0}))(i,this._sortColumns[this._sortColumn],this._sortDirection,this._sortColumn):i,[o]=await Promise.all([n,rt]),s=(new Date).getTime()-e;if(s<100&&await new Promise(e=>setTimeout(e,100-s)),this.curRequest===t){if(this.appendRow||this.hasFab){const e=[...o];this.appendRow&&e.push({append:!0,content:this.appendRow}),this.hasFab&&e.push({empty:!0}),this._items=e}else this._items=o;this._filteredData=o}}},{kind:"field",key:"_memFilterData",value:()=>B(async(e,t,i)=>((e,t,i)=>(i=i.toUpperCase(),e.filter(e=>Object.entries(t).some(t=>{const[n,o]=t;return!(!o.filterable||!String(o.filterKey?e[o.valueColumn||n][o.filterKey]:e[o.valueColumn||n]).toUpperCase().includes(i))}))))(e,t,i))},{kind:"method",key:"_handleHeaderClick",value:function(e){const t=e.currentTarget.columnId;this.columns[t].sortable&&(this._sortDirection&&this._sortColumn===t?"asc"===this._sortDirection?this._sortDirection="desc":"desc"===this._sortDirection?this._sortDirection="asc":this._sortDirection=null:this._sortDirection="asc",this._sortColumn=null===this._sortDirection?void 0:t,S(this,"sorting-changed",{column:t,direction:this._sortDirection}))}},{kind:"method",key:"_handleHeaderRowCheckboxClick",value:function(e){e.target.checked?(this._checkedRows=this._filteredData.filter(e=>!1!==e.selectable).map(e=>e[this.id]),this._checkedRowsChanged()):(this._checkedRows=[],this._checkedRowsChanged())}},{kind:"method",key:"_handleRowCheckboxClick",value:function(e){const t=e.currentTarget,i=t.rowId;if(t.checked){if(this._checkedRows.includes(i))return;this._checkedRows=[...this._checkedRows,i]}else this._checkedRows=this._checkedRows.filter(e=>e!==i);this._checkedRowsChanged()}},{kind:"method",key:"_handleRowClick",value:function(e){const t=e.target;if(["HA-CHECKBOX","MWC-BUTTON"].includes(t.tagName))return;const i=e.currentTarget.rowId;S(this,"row-click",{id:i},{bubbles:!1})}},{kind:"method",key:"_checkedRowsChanged",value:function(){this._items.length&&(this._items=[...this._items]),S(this,"selection-changed",{value:this._checkedRows})}},{kind:"method",key:"_handleSearchChange",value:function(e){this._debounceSearch(e.detail.value)}},{kind:"method",key:"_calcTableHeight",value:async function(){this.autoHeight||(await this.updateComplete,this._headerHeight=this._header.clientHeight)}},{kind:"method",decorators:[R({passive:!0})],key:"_saveScrollPos",value:function(e){this._savedScrollPos=e.target.scrollTop}},{kind:"get",static:!0,key:"styles",value:function(){return[$,h`
        /* default mdc styles, colors changed, without checkbox styles */
        :host {
          height: 100%;
        }
        .mdc-data-table__content {
          font-family: Roboto, sans-serif;
          -moz-osx-font-smoothing: grayscale;
          -webkit-font-smoothing: antialiased;
          font-size: 0.875rem;
          line-height: 1.25rem;
          font-weight: 400;
          letter-spacing: 0.0178571429em;
          text-decoration: inherit;
          text-transform: inherit;
        }

        .mdc-data-table {
          background-color: var(--data-table-background-color);
          border-radius: 4px;
          border-width: 1px;
          border-style: solid;
          border-color: var(--divider-color);
          display: inline-flex;
          flex-direction: column;
          box-sizing: border-box;
          overflow: hidden;
        }

        .mdc-data-table__row--selected {
          background-color: rgba(var(--rgb-primary-color), 0.04);
        }

        .mdc-data-table__row {
          display: flex;
          width: 100%;
          height: 52px;
        }

        .mdc-data-table__row ~ .mdc-data-table__row {
          border-top: 1px solid var(--divider-color);
        }

        .mdc-data-table__row:not(.mdc-data-table__row--selected):hover {
          background-color: rgba(var(--rgb-primary-text-color), 0.04);
        }

        .mdc-data-table__header-cell {
          color: var(--primary-text-color);
        }

        .mdc-data-table__cell {
          color: var(--primary-text-color);
        }

        .mdc-data-table__header-row {
          height: 56px;
          display: flex;
          width: 100%;
          border-bottom: 1px solid var(--divider-color);
          overflow-x: auto;
        }

        .mdc-data-table__header-row::-webkit-scrollbar {
          display: none;
        }

        .mdc-data-table__cell,
        .mdc-data-table__header-cell {
          padding-right: 16px;
          padding-left: 16px;
          align-self: center;
          overflow: hidden;
          text-overflow: ellipsis;
          flex-shrink: 0;
          box-sizing: border-box;
        }

        .mdc-data-table__cell.mdc-data-table__cell--icon {
          overflow: initial;
        }

        .mdc-data-table__header-cell--checkbox,
        .mdc-data-table__cell--checkbox {
          /* @noflip */
          padding-left: 16px;
          /* @noflip */
          padding-right: 0;
          width: 56px;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell--checkbox,
        :host([dir="rtl"]) .mdc-data-table__cell--checkbox {
          /* @noflip */
          padding-left: 0;
          /* @noflip */
          padding-right: 16px;
        }

        .mdc-data-table__table {
          height: 100%;
          width: 100%;
          border: 0;
          white-space: nowrap;
        }

        .mdc-data-table__cell {
          font-family: Roboto, sans-serif;
          -moz-osx-font-smoothing: grayscale;
          -webkit-font-smoothing: antialiased;
          font-size: 0.875rem;
          line-height: 1.25rem;
          font-weight: 400;
          letter-spacing: 0.0178571429em;
          text-decoration: inherit;
          text-transform: inherit;
        }

        .mdc-data-table__cell a {
          color: inherit;
          text-decoration: none;
        }

        .mdc-data-table__cell--numeric {
          text-align: right;
        }
        :host([dir="rtl"]) .mdc-data-table__cell--numeric {
          /* @noflip */
          text-align: left;
        }

        .mdc-data-table__cell--icon {
          color: var(--secondary-text-color);
          text-align: center;
        }

        .mdc-data-table__header-cell--icon,
        .mdc-data-table__cell--icon {
          width: 54px;
        }

        .mdc-data-table__header-cell.mdc-data-table__header-cell--icon {
          text-align: center;
        }

        .mdc-data-table__header-cell.sortable.mdc-data-table__header-cell--icon:hover,
        .mdc-data-table__header-cell.sortable.mdc-data-table__header-cell--icon:not(.not-sorted) {
          text-align: left;
        }
        :host([dir="rtl"])
          .mdc-data-table__header-cell.sortable.mdc-data-table__header-cell--icon:hover,
        :host([dir="rtl"])
          .mdc-data-table__header-cell.sortable.mdc-data-table__header-cell--icon:not(.not-sorted) {
          text-align: right;
        }

        .mdc-data-table__cell--icon:first-child ha-icon,
        .mdc-data-table__cell--icon:first-child ha-state-icon,
        .mdc-data-table__cell--icon:first-child ha-svg-icon {
          margin-left: 8px;
        }
        :host([dir="rtl"]) .mdc-data-table__cell--icon:first-child ha-icon,
        :host([dir="rtl"]) .mdc-data-table__cell--icon:first-child ha-state-icon,
        :host([dir="rtl"]) .mdc-data-table__cell--icon:first-child ha-svg-icon {
          margin-left: auto;
          margin-right: 8px;
        }

        .mdc-data-table__cell--icon:first-child state-badge {
          margin-right: -8px;
        }
        :host([dir="rtl"]) .mdc-data-table__cell--icon:first-child state-badge {
          margin-right: auto;
          margin-left: -8px;
        }

        .mdc-data-table__cell--overflow-menu,
        .mdc-data-table__header-cell--overflow-menu,
        .mdc-data-table__header-cell--icon-button,
        .mdc-data-table__cell--icon-button {
          padding: 8px;
        }

        .mdc-data-table__header-cell--icon-button,
        .mdc-data-table__cell--icon-button {
          width: 56px;
        }

        .mdc-data-table__cell--overflow-menu,
        .mdc-data-table__cell--icon-button {
          color: var(--secondary-text-color);
          text-overflow: clip;
        }

        .mdc-data-table__header-cell--icon-button:first-child,
        .mdc-data-table__cell--icon-button:first-child,
        .mdc-data-table__header-cell--icon-button:last-child,
        .mdc-data-table__cell--icon-button:last-child {
          width: 64px;
        }

        .mdc-data-table__cell--overflow-menu:first-child,
        .mdc-data-table__header-cell--overflow-menu:first-child,
        .mdc-data-table__header-cell--icon-button:first-child,
        .mdc-data-table__cell--icon-button:first-child {
          padding-left: 16px;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell--overflow-menu:first-child,
        :host([dir="rtl"]) .mdc-data-table__cell--overflow-menu:first-child,
        :host([dir="rtl"]) .mdc-data-table__header-cell--overflow-menu:first-child,
        :host([dir="rtl"]) .mdc-data-table__cell--overflow-menu:first-child {
          padding-left: 8px;
          padding-right: 16px;
        }

        .mdc-data-table__cell--overflow-menu:last-child,
        .mdc-data-table__header-cell--overflow-menu:last-child,
        .mdc-data-table__header-cell--icon-button:last-child,
        .mdc-data-table__cell--icon-button:last-child {
          padding-right: 16px;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell--overflow-menu:last-child,
        :host([dir="rtl"]) .mdc-data-table__cell--overflow-menu:last-child,
        :host([dir="rtl"]) .mdc-data-table__header-cell--icon-button:last-child,
        :host([dir="rtl"]) .mdc-data-table__cell--icon-button:last-child {
          padding-right: 8px;
          padding-left: 16px;
        }
        .mdc-data-table__cell--overflow-menu,
        .mdc-data-table__header-cell--overflow-menu {
          overflow: initial;
        }
        .mdc-data-table__cell--icon-button a {
          color: var(--secondary-text-color);
        }

        .mdc-data-table__header-cell {
          font-family: Roboto, sans-serif;
          -moz-osx-font-smoothing: grayscale;
          -webkit-font-smoothing: antialiased;
          font-size: 0.875rem;
          line-height: 1.375rem;
          font-weight: 500;
          letter-spacing: 0.0071428571em;
          text-decoration: inherit;
          text-transform: inherit;
          text-align: left;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell {
          /* @noflip */
          text-align: right;
        }

        .mdc-data-table__header-cell--numeric {
          text-align: right;
        }
        .mdc-data-table__header-cell--numeric.sortable:hover,
        .mdc-data-table__header-cell--numeric.sortable:not(.not-sorted) {
          text-align: left;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell--numeric {
          /* @noflip */
          text-align: left;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell--numeric.sortable:hover,
        :host([dir="rtl"]) .mdc-data-table__header-cell--numeric.sortable:not(.not-sorted) {
          text-align: right;
        }

        /* custom from here */

        :host {
          display: block;
        }

        .mdc-data-table {
          display: block;
          border-width: var(--data-table-border-width, 1px);
          height: 100%;
        }
        .mdc-data-table__header-cell {
          overflow: hidden;
          position: relative;
        }
        .mdc-data-table__header-cell span {
          position: relative;
          left: 0px;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell span {
          left: auto;
          right: 0px;
        }

        .mdc-data-table__header-cell.sortable {
          cursor: pointer;
        }
        .mdc-data-table__header-cell > * {
          transition: left 0.2s ease;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell > * {
          transition: right 0.2s ease;
        }
        .mdc-data-table__header-cell ha-svg-icon {
          top: -3px;
          position: absolute;
        }
        .mdc-data-table__header-cell.not-sorted ha-svg-icon {
          left: -20px;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell.not-sorted ha-svg-icon {
          right: -20px;
        }
        .mdc-data-table__header-cell.sortable:not(.not-sorted) span,
        .mdc-data-table__header-cell.sortable.not-sorted:hover span {
          left: 24px;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell.sortable:not(.not-sorted) span,
        :host([dir="rtl"]) .mdc-data-table__header-cell.sortable.not-sorted:hover span {
          left: auto;
          right: 24px;
        }
        .mdc-data-table__header-cell.sortable:not(.not-sorted) ha-svg-icon,
        .mdc-data-table__header-cell.sortable:hover.not-sorted ha-svg-icon {
          left: 12px;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell.sortable:not(.not-sorted) ha-svg-icon,
        :host([dir="rtl"]) .mdc-data-table__header-cell.sortable:hover.not-sorted ha-svg-icon {
          left: auto;
          right: 12px;
        }
        .table-header {
          border-bottom: 1px solid var(--divider-color);
          padding: 0 16px;
        }
        search-input {
          position: relative;
          top: 2px;
        }
        slot[name="header"] {
          display: block;
        }
        .center {
          text-align: center;
        }
        .secondary {
          color: var(--secondary-text-color);
        }
        .scroller {
          height: calc(100% - 57px);
        }

        .mdc-data-table__table.auto-height .scroller {
          overflow-y: hidden !important;
        }
        .grows {
          flex-grow: 1;
          flex-shrink: 1;
        }
        .forceLTR {
          direction: ltr;
        }
        .clickable {
          cursor: pointer;
        }
      `]}}]}}),r);var _t={UNKNOWN:"Unknown",BACKSPACE:"Backspace",ENTER:"Enter",SPACEBAR:"Spacebar",PAGE_UP:"PageUp",PAGE_DOWN:"PageDown",END:"End",HOME:"Home",ARROW_LEFT:"ArrowLeft",ARROW_UP:"ArrowUp",ARROW_RIGHT:"ArrowRight",ARROW_DOWN:"ArrowDown",DELETE:"Delete",ESCAPE:"Escape",TAB:"Tab"},bt=new Set;bt.add(_t.BACKSPACE),bt.add(_t.ENTER),bt.add(_t.SPACEBAR),bt.add(_t.PAGE_UP),bt.add(_t.PAGE_DOWN),bt.add(_t.END),bt.add(_t.HOME),bt.add(_t.ARROW_LEFT),bt.add(_t.ARROW_UP),bt.add(_t.ARROW_RIGHT),bt.add(_t.ARROW_DOWN),bt.add(_t.DELETE),bt.add(_t.ESCAPE),bt.add(_t.TAB);var ft=8,gt=13,vt=32,yt=33,xt=34,kt=35,wt=36,Et=37,It=38,Ct=39,St=40,Tt=46,At=27,Rt=9,Ot=new Map;Ot.set(ft,_t.BACKSPACE),Ot.set(gt,_t.ENTER),Ot.set(vt,_t.SPACEBAR),Ot.set(yt,_t.PAGE_UP),Ot.set(xt,_t.PAGE_DOWN),Ot.set(kt,_t.END),Ot.set(wt,_t.HOME),Ot.set(Et,_t.ARROW_LEFT),Ot.set(It,_t.ARROW_UP),Ot.set(Ct,_t.ARROW_RIGHT),Ot.set(St,_t.ARROW_DOWN),Ot.set(Tt,_t.DELETE),Ot.set(At,_t.ESCAPE),Ot.set(Rt,_t.TAB);var Ft,zt,Mt=new Set;function Lt(e){var t=e.key;if(bt.has(t))return t;var i=Ot.get(e.keyCode);return i||_t.UNKNOWN}Mt.add(_t.PAGE_UP),Mt.add(_t.PAGE_DOWN),Mt.add(_t.END),Mt.add(_t.HOME),Mt.add(_t.ARROW_LEFT),Mt.add(_t.ARROW_UP),Mt.add(_t.ARROW_RIGHT),Mt.add(_t.ARROW_DOWN);var Dt="mdc-list-item--activated",Bt="mdc-list-item",$t="mdc-list-item--disabled",Pt="mdc-list-item--selected",Nt="mdc-list-item__text",Ht="mdc-list-item__primary-text",Vt="mdc-list";(Ft={})[""+Dt]="mdc-list-item--activated",Ft[""+Bt]="mdc-list-item",Ft[""+$t]="mdc-list-item--disabled",Ft[""+Pt]="mdc-list-item--selected",Ft[""+Ht]="mdc-list-item__primary-text",Ft[""+Vt]="mdc-list";var Ut=((zt={})[""+Dt]="mdc-deprecated-list-item--activated",zt[""+Bt]="mdc-deprecated-list-item",zt[""+$t]="mdc-deprecated-list-item--disabled",zt[""+Pt]="mdc-deprecated-list-item--selected",zt[""+Nt]="mdc-deprecated-list-item__text",zt[""+Ht]="mdc-deprecated-list-item__primary-text",zt[""+Vt]="mdc-deprecated-list",zt),Kt={ACTION_EVENT:"MDCList:action",ARIA_CHECKED:"aria-checked",ARIA_CHECKED_CHECKBOX_SELECTOR:'[role="checkbox"][aria-checked="true"]',ARIA_CHECKED_RADIO_SELECTOR:'[role="radio"][aria-checked="true"]',ARIA_CURRENT:"aria-current",ARIA_DISABLED:"aria-disabled",ARIA_ORIENTATION:"aria-orientation",ARIA_ORIENTATION_HORIZONTAL:"horizontal",ARIA_ROLE_CHECKBOX_SELECTOR:'[role="checkbox"]',ARIA_SELECTED:"aria-selected",ARIA_INTERACTIVE_ROLES_SELECTOR:'[role="listbox"], [role="menu"]',ARIA_MULTI_SELECTABLE_SELECTOR:'[aria-multiselectable="true"]',CHECKBOX_RADIO_SELECTOR:'input[type="checkbox"], input[type="radio"]',CHECKBOX_SELECTOR:'input[type="checkbox"]',CHILD_ELEMENTS_TO_TOGGLE_TABINDEX:"\n    ."+Bt+" button:not(:disabled),\n    ."+Bt+" a,\n    ."+Ut[Bt]+" button:not(:disabled),\n    ."+Ut[Bt]+" a\n  ",DEPRECATED_SELECTOR:".mdc-deprecated-list",FOCUSABLE_CHILD_ELEMENTS:"\n    ."+Bt+" button:not(:disabled),\n    ."+Bt+" a,\n    ."+Bt+' input[type="radio"]:not(:disabled),\n    .'+Bt+' input[type="checkbox"]:not(:disabled),\n    .'+Ut[Bt]+" button:not(:disabled),\n    ."+Ut[Bt]+" a,\n    ."+Ut[Bt]+' input[type="radio"]:not(:disabled),\n    .'+Ut[Bt]+' input[type="checkbox"]:not(:disabled)\n  ',RADIO_SELECTOR:'input[type="radio"]',SELECTED_ITEM_SELECTOR:'[aria-selected="true"], [aria-current="true"]'},Wt={UNSET_INDEX:-1,TYPEAHEAD_BUFFER_CLEAR_TIMEOUT_MS:300};const Gt=(e,t)=>e-t,jt=["input","button","textarea","select"];function qt(e){return e instanceof Set}const Xt=e=>{const t=e===Wt.UNSET_INDEX?new Set:e;return qt(t)?new Set(t):new Set([t])};class Qt extends P{constructor(e){super(Object.assign(Object.assign({},Qt.defaultAdapter),e)),this.isMulti_=!1,this.wrapFocus_=!1,this.isVertical_=!0,this.selectedIndex_=Wt.UNSET_INDEX,this.focusedItemIndex_=Wt.UNSET_INDEX,this.useActivatedClass_=!1,this.ariaCurrentAttrValue_=null}static get strings(){return Kt}static get numbers(){return Wt}static get defaultAdapter(){return{focusItemAtIndex:()=>{},getFocusedElementIndex:()=>0,getListItemCount:()=>0,isFocusInsideList:()=>!1,isRootFocused:()=>!1,notifyAction:()=>{},notifySelected:()=>{},getSelectedStateForElementIndex:()=>!1,setDisabledStateForElementIndex:()=>{},getDisabledStateForElementIndex:()=>!1,setSelectedStateForElementIndex:()=>{},setActivatedStateForElementIndex:()=>{},setTabIndexForElementIndex:()=>{},setAttributeForElementIndex:()=>{},getAttributeForElementIndex:()=>null}}setWrapFocus(e){this.wrapFocus_=e}setMulti(e){this.isMulti_=e;const t=this.selectedIndex_;if(e){if(!qt(t)){const e=t===Wt.UNSET_INDEX;this.selectedIndex_=e?new Set:new Set([t])}}else if(qt(t))if(t.size){const e=Array.from(t).sort(Gt);this.selectedIndex_=e[0]}else this.selectedIndex_=Wt.UNSET_INDEX}setVerticalOrientation(e){this.isVertical_=e}setUseActivatedClass(e){this.useActivatedClass_=e}getSelectedIndex(){return this.selectedIndex_}setSelectedIndex(e){this.isIndexValid_(e)&&(this.isMulti_?this.setMultiSelectionAtIndex_(Xt(e)):this.setSingleSelectionAtIndex_(e))}handleFocusIn(e,t){t>=0&&this.adapter.setTabIndexForElementIndex(t,0)}handleFocusOut(e,t){t>=0&&this.adapter.setTabIndexForElementIndex(t,-1),setTimeout(()=>{this.adapter.isFocusInsideList()||this.setTabindexToFirstSelectedItem_()},0)}handleKeydown(e,t,i){const n="ArrowLeft"===Lt(e),o="ArrowUp"===Lt(e),s="ArrowRight"===Lt(e),a="ArrowDown"===Lt(e),r="Home"===Lt(e),c="End"===Lt(e),l="Enter"===Lt(e),d="Spacebar"===Lt(e);if(this.adapter.isRootFocused())return void(o||c?(e.preventDefault(),this.focusLastElement()):(a||r)&&(e.preventDefault(),this.focusFirstElement()));let h,p=this.adapter.getFocusedElementIndex();if(!(-1===p&&(p=i,p<0))){if(this.isVertical_&&a||!this.isVertical_&&s)this.preventDefaultEvent(e),h=this.focusNextElement(p);else if(this.isVertical_&&o||!this.isVertical_&&n)this.preventDefaultEvent(e),h=this.focusPrevElement(p);else if(r)this.preventDefaultEvent(e),h=this.focusFirstElement();else if(c)this.preventDefaultEvent(e),h=this.focusLastElement();else if((l||d)&&t){const t=e.target;if(t&&"A"===t.tagName&&l)return;this.preventDefaultEvent(e),this.setSelectedIndexOnAction_(p,!0)}this.focusedItemIndex_=p,void 0!==h&&(this.setTabindexAtIndex_(h),this.focusedItemIndex_=h)}}handleSingleSelection(e,t,i){e!==Wt.UNSET_INDEX&&(this.setSelectedIndexOnAction_(e,t,i),this.setTabindexAtIndex_(e),this.focusedItemIndex_=e)}focusNextElement(e){let t=e+1;if(t>=this.adapter.getListItemCount()){if(!this.wrapFocus_)return e;t=0}return this.adapter.focusItemAtIndex(t),t}focusPrevElement(e){let t=e-1;if(t<0){if(!this.wrapFocus_)return e;t=this.adapter.getListItemCount()-1}return this.adapter.focusItemAtIndex(t),t}focusFirstElement(){return this.adapter.focusItemAtIndex(0),0}focusLastElement(){const e=this.adapter.getListItemCount()-1;return this.adapter.focusItemAtIndex(e),e}setEnabled(e,t){this.isIndexValid_(e)&&this.adapter.setDisabledStateForElementIndex(e,!t)}preventDefaultEvent(e){const t=(""+e.target.tagName).toLowerCase();-1===jt.indexOf(t)&&e.preventDefault()}setSingleSelectionAtIndex_(e,t=!0){this.selectedIndex_!==e&&(this.selectedIndex_!==Wt.UNSET_INDEX&&(this.adapter.setSelectedStateForElementIndex(this.selectedIndex_,!1),this.useActivatedClass_&&this.adapter.setActivatedStateForElementIndex(this.selectedIndex_,!1)),t&&this.adapter.setSelectedStateForElementIndex(e,!0),this.useActivatedClass_&&this.adapter.setActivatedStateForElementIndex(e,!0),this.setAriaForSingleSelectionAtIndex_(e),this.selectedIndex_=e,this.adapter.notifySelected(e))}setMultiSelectionAtIndex_(e,t=!0){const i=((e,t)=>{const i=Array.from(e),n=Array.from(t),o={added:[],removed:[]},s=i.sort(Gt),a=n.sort(Gt);let r=0,c=0;for(;r<s.length||c<a.length;){const e=s[r],t=a[c];e!==t?void 0!==e&&(void 0===t||e<t)?(o.removed.push(e),r++):void 0!==t&&(void 0===e||t<e)&&(o.added.push(t),c++):(r++,c++)}return o})(Xt(this.selectedIndex_),e);if(i.removed.length||i.added.length){for(const e of i.removed)t&&this.adapter.setSelectedStateForElementIndex(e,!1),this.useActivatedClass_&&this.adapter.setActivatedStateForElementIndex(e,!1);for(const e of i.added)t&&this.adapter.setSelectedStateForElementIndex(e,!0),this.useActivatedClass_&&this.adapter.setActivatedStateForElementIndex(e,!0);this.selectedIndex_=e,this.adapter.notifySelected(e,i)}}setAriaForSingleSelectionAtIndex_(e){this.selectedIndex_===Wt.UNSET_INDEX&&(this.ariaCurrentAttrValue_=this.adapter.getAttributeForElementIndex(e,Kt.ARIA_CURRENT));const t=null!==this.ariaCurrentAttrValue_,i=t?Kt.ARIA_CURRENT:Kt.ARIA_SELECTED;this.selectedIndex_!==Wt.UNSET_INDEX&&this.adapter.setAttributeForElementIndex(this.selectedIndex_,i,"false");const n=t?this.ariaCurrentAttrValue_:"true";this.adapter.setAttributeForElementIndex(e,i,n)}setTabindexAtIndex_(e){this.focusedItemIndex_===Wt.UNSET_INDEX&&0!==e?this.adapter.setTabIndexForElementIndex(0,-1):this.focusedItemIndex_>=0&&this.focusedItemIndex_!==e&&this.adapter.setTabIndexForElementIndex(this.focusedItemIndex_,-1),this.adapter.setTabIndexForElementIndex(e,0)}setTabindexToFirstSelectedItem_(){let e=0;"number"==typeof this.selectedIndex_&&this.selectedIndex_!==Wt.UNSET_INDEX?e=this.selectedIndex_:qt(this.selectedIndex_)&&this.selectedIndex_.size>0&&(e=Math.min(...this.selectedIndex_)),this.setTabindexAtIndex_(e)}isIndexValid_(e){if(e instanceof Set){if(!this.isMulti_)throw new Error("MDCListFoundation: Array of index is only supported for checkbox based list");if(0===e.size)return!0;{let t=!1;for(const i of e)if(t=this.isIndexInRange_(i),t)break;return t}}if("number"==typeof e){if(this.isMulti_)throw new Error("MDCListFoundation: Expected array of index for checkbox based list but got number: "+e);return e===Wt.UNSET_INDEX||this.isIndexInRange_(e)}return!1}isIndexInRange_(e){const t=this.adapter.getListItemCount();return e>=0&&e<t}setSelectedIndexOnAction_(e,t,i){if(this.adapter.getDisabledStateForElementIndex(e))return;let n=e;if(this.isMulti_&&(n=new Set([e])),this.isIndexValid_(n)){if(this.isMulti_)this.toggleMultiAtIndex(e,i,t);else if(t||i)this.setSingleSelectionAtIndex_(e,t);else{this.selectedIndex_===e&&this.setSingleSelectionAtIndex_(Wt.UNSET_INDEX)}t&&this.adapter.notifyAction(e)}}toggleMultiAtIndex(e,t,i=!0){let n=!1;n=void 0===t?!this.adapter.getSelectedStateForElementIndex(e):t;const o=Xt(this.selectedIndex_);n?o.add(e):o.delete(e),this.setMultiSelectionAtIndex_(o,i)}}const Yt=e=>e.hasAttribute("mwc-list-item");function Zt(){const e=this.itemsReadyResolver;this.itemsReady=new Promise(e=>this.itemsReadyResolver=e),e()}class Jt extends T{constructor(){super(),this.mdcAdapter=null,this.mdcFoundationClass=Qt,this.activatable=!1,this.multi=!1,this.wrapFocus=!1,this.itemRoles=null,this.innerRole=null,this.innerAriaLabel=null,this.rootTabbable=!1,this.previousTabindex=null,this.noninteractive=!1,this.itemsReadyResolver=()=>{},this.itemsReady=Promise.resolve([]),this.items_=[];const e=function(e,t=50){let i;return function(n=!0){clearTimeout(i),i=setTimeout(()=>{e(n)},t)}}(this.layout.bind(this));this.debouncedLayout=(t=!0)=>{Zt.call(this),e(t)}}async getUpdateComplete(){const e=await super.getUpdateComplete();return await this.itemsReady,e}get items(){return this.items_}updateItems(){var e;const t=null!==(e=this.assignedElements)&&void 0!==e?e:[],i=[];for(const e of t)Yt(e)&&(i.push(e),e._managingList=this),e.hasAttribute("divider")&&!e.hasAttribute("role")&&e.setAttribute("role","separator");this.items_=i;const n=new Set;if(this.items_.forEach((e,t)=>{this.itemRoles?e.setAttribute("role",this.itemRoles):e.removeAttribute("role"),e.selected&&n.add(t)}),this.multi)this.select(n);else{const e=n.size?n.entries().next().value[1]:-1;this.select(e)}const o=new Event("items-updated",{bubbles:!0,composed:!0});this.dispatchEvent(o)}get selected(){const e=this.index;if(!qt(e))return-1===e?null:this.items[e];const t=[];for(const i of e)t.push(this.items[i]);return t}get index(){return this.mdcFoundation?this.mdcFoundation.getSelectedIndex():-1}render(){const e=null===this.innerRole?void 0:this.innerRole,t=null===this.innerAriaLabel?void 0:this.innerAriaLabel,i=this.rootTabbable?"0":"-1";return l`
      <!-- @ts-ignore -->
      <ul
          tabindex=${i}
          role="${O(e)}"
          aria-label="${O(t)}"
          class="mdc-deprecated-list"
          @keydown=${this.onKeydown}
          @focusin=${this.onFocusIn}
          @focusout=${this.onFocusOut}
          @request-selected=${this.onRequestSelected}
          @list-item-rendered=${this.onListItemConnected}>
        <slot></slot>
        ${this.renderPlaceholder()}
      </ul>
    `}renderPlaceholder(){var e;const t=null!==(e=this.assignedElements)&&void 0!==e?e:[];return void 0!==this.emptyMessage&&0===t.length?l`
        <mwc-list-item noninteractive>${this.emptyMessage}</mwc-list-item>
      `:null}firstUpdated(){super.firstUpdated(),this.items.length||(this.mdcFoundation.setMulti(this.multi),this.layout())}onFocusIn(e){if(this.mdcFoundation&&this.mdcRoot){const t=this.getIndexOfTarget(e);this.mdcFoundation.handleFocusIn(e,t)}}onFocusOut(e){if(this.mdcFoundation&&this.mdcRoot){const t=this.getIndexOfTarget(e);this.mdcFoundation.handleFocusOut(e,t)}}onKeydown(e){if(this.mdcFoundation&&this.mdcRoot){const t=this.getIndexOfTarget(e),i=e.target,n=Yt(i);this.mdcFoundation.handleKeydown(e,n,t)}}onRequestSelected(e){if(this.mdcFoundation){let t=this.getIndexOfTarget(e);if(-1===t&&(this.layout(),t=this.getIndexOfTarget(e),-1===t))return;if(this.items[t].disabled)return;const i=e.detail.selected,n=e.detail.source;this.mdcFoundation.handleSingleSelection(t,"interaction"===n,i),e.stopPropagation()}}getIndexOfTarget(e){const t=this.items,i=e.composedPath();for(const e of i){let i=-1;if(N(e)&&Yt(e)&&(i=t.indexOf(e)),-1!==i)return i}return-1}createAdapter(){return this.mdcAdapter={getListItemCount:()=>this.mdcRoot?this.items.length:0,getFocusedElementIndex:this.getFocusedItemIndex,getAttributeForElementIndex:(e,t)=>{if(!this.mdcRoot)return"";const i=this.items[e];return i?i.getAttribute(t):""},setAttributeForElementIndex:(e,t,i)=>{if(!this.mdcRoot)return;const n=this.items[e];n&&n.setAttribute(t,i)},focusItemAtIndex:e=>{const t=this.items[e];t&&t.focus()},setTabIndexForElementIndex:(e,t)=>{const i=this.items[e];i&&(i.tabindex=t)},notifyAction:e=>{const t={bubbles:!0,composed:!0};t.detail={index:e};const i=new CustomEvent("action",t);this.dispatchEvent(i)},notifySelected:(e,t)=>{const i={bubbles:!0,composed:!0};i.detail={index:e,diff:t};const n=new CustomEvent("selected",i);this.dispatchEvent(n)},isFocusInsideList:()=>H(this),isRootFocused:()=>{const e=this.mdcRoot;return e.getRootNode().activeElement===e},setDisabledStateForElementIndex:(e,t)=>{const i=this.items[e];i&&(i.disabled=t)},getDisabledStateForElementIndex:e=>{const t=this.items[e];return!!t&&t.disabled},setSelectedStateForElementIndex:(e,t)=>{const i=this.items[e];i&&(i.selected=t)},getSelectedStateForElementIndex:e=>{const t=this.items[e];return!!t&&t.selected},setActivatedStateForElementIndex:(e,t)=>{const i=this.items[e];i&&(i.activated=t)}},this.mdcAdapter}selectUi(e,t=!1){const i=this.items[e];i&&(i.selected=!0,i.activated=t)}deselectUi(e){const t=this.items[e];t&&(t.selected=!1,t.activated=!1)}select(e){this.mdcFoundation&&this.mdcFoundation.setSelectedIndex(e)}toggle(e,t){this.multi&&this.mdcFoundation.toggleMultiAtIndex(e,t)}onListItemConnected(e){const t=e.target;this.layout(-1===this.items.indexOf(t))}layout(e=!0){e&&this.updateItems();const t=this.items[0];for(const e of this.items)e.tabindex=-1;t&&(this.noninteractive?this.previousTabindex||(this.previousTabindex=t):t.tabindex=0),this.itemsReadyResolver()}getFocusedItemIndex(){if(!this.mdcRoot)return-1;if(!this.items.length)return-1;const e=V();if(!e.length)return-1;for(let t=e.length-1;t>=0;t--){const i=e[t];if(Yt(i))return this.items.indexOf(i)}return-1}focusItemAtIndex(e){for(const e of this.items)if(0===e.tabindex){e.tabindex=-1;break}this.items[e].tabindex=0,this.items[e].focus()}focus(){const e=this.mdcRoot;e&&e.focus()}blur(){const e=this.mdcRoot;e&&e.blur()}}i([s({type:String})],Jt.prototype,"emptyMessage",void 0),i([n(".mdc-deprecated-list")],Jt.prototype,"mdcRoot",void 0),i([j("",!0,"*")],Jt.prototype,"assignedElements",void 0),i([j("",!0,'[tabindex="0"]')],Jt.prototype,"tabbableElements",void 0),i([s({type:Boolean}),q((function(e){this.mdcFoundation&&this.mdcFoundation.setUseActivatedClass(e)}))],Jt.prototype,"activatable",void 0),i([s({type:Boolean}),q((function(e,t){this.mdcFoundation&&this.mdcFoundation.setMulti(e),void 0!==t&&this.layout()}))],Jt.prototype,"multi",void 0),i([s({type:Boolean}),q((function(e){this.mdcFoundation&&this.mdcFoundation.setWrapFocus(e)}))],Jt.prototype,"wrapFocus",void 0),i([s({type:String}),q((function(e,t){void 0!==t&&this.updateItems()}))],Jt.prototype,"itemRoles",void 0),i([s({type:String})],Jt.prototype,"innerRole",void 0),i([s({type:String})],Jt.prototype,"innerAriaLabel",void 0),i([s({type:Boolean})],Jt.prototype,"rootTabbable",void 0),i([s({type:Boolean,reflect:!0}),q((function(e){var t,i;if(e){const e=null!==(i=null===(t=this.tabbableElements)||void 0===t?void 0:t[0])&&void 0!==i?i:null;this.previousTabindex=e,e&&e.setAttribute("tabindex","-1")}else!e&&this.previousTabindex&&(this.previousTabindex.setAttribute("tabindex","0"),this.previousTabindex=null)}))],Jt.prototype,"noninteractive",void 0);const ei=h`@keyframes mdc-ripple-fg-radius-in{from{animation-timing-function:cubic-bezier(0.4, 0, 0.2, 1);transform:translate(var(--mdc-ripple-fg-translate-start, 0)) scale(1)}to{transform:translate(var(--mdc-ripple-fg-translate-end, 0)) scale(var(--mdc-ripple-fg-scale, 1))}}@keyframes mdc-ripple-fg-opacity-in{from{animation-timing-function:linear;opacity:0}to{opacity:var(--mdc-ripple-fg-opacity, 0)}}@keyframes mdc-ripple-fg-opacity-out{from{animation-timing-function:linear;opacity:var(--mdc-ripple-fg-opacity, 0)}to{opacity:0}}:host{display:block}.mdc-deprecated-list{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-subtitle1-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:1rem;font-size:var(--mdc-typography-subtitle1-font-size, 1rem);line-height:1.75rem;line-height:var(--mdc-typography-subtitle1-line-height, 1.75rem);font-weight:400;font-weight:var(--mdc-typography-subtitle1-font-weight, 400);letter-spacing:0.009375em;letter-spacing:var(--mdc-typography-subtitle1-letter-spacing, 0.009375em);text-decoration:inherit;text-decoration:var(--mdc-typography-subtitle1-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-subtitle1-text-transform, inherit);line-height:1.5rem;margin:0;padding:8px 0;list-style-type:none;color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87));padding:var(--mdc-list-vertical-padding, 8px) 0}.mdc-deprecated-list:focus{outline:none}.mdc-deprecated-list-item{height:48px}.mdc-deprecated-list--dense{padding-top:4px;padding-bottom:4px;font-size:.812rem}.mdc-deprecated-list ::slotted([divider]){height:0;margin:0;border:none;border-bottom-width:1px;border-bottom-style:solid;border-bottom-color:rgba(0, 0, 0, 0.12)}.mdc-deprecated-list ::slotted([divider][padded]){margin:0 var(--mdc-list-side-padding, 16px)}.mdc-deprecated-list ::slotted([divider][inset]){margin-left:var(--mdc-list-inset-margin, 72px);margin-right:0;width:calc( 100% - var(--mdc-list-inset-margin, 72px) )}[dir=rtl] .mdc-deprecated-list ::slotted([divider][inset]),.mdc-deprecated-list ::slotted([divider][inset][dir=rtl]){margin-left:0;margin-right:var(--mdc-list-inset-margin, 72px)}.mdc-deprecated-list ::slotted([divider][inset][padded]){width:calc( 100% - var(--mdc-list-inset-margin, 72px) - var(--mdc-list-side-padding, 16px) )}.mdc-deprecated-list--dense ::slotted([mwc-list-item]){height:40px}.mdc-deprecated-list--dense ::slotted([mwc-list]){--mdc-list-item-graphic-size: 20px}.mdc-deprecated-list--two-line.mdc-deprecated-list--dense ::slotted([mwc-list-item]),.mdc-deprecated-list--avatar-list.mdc-deprecated-list--dense ::slotted([mwc-list-item]){height:60px}.mdc-deprecated-list--avatar-list.mdc-deprecated-list--dense ::slotted([mwc-list]){--mdc-list-item-graphic-size: 36px}:host([noninteractive]){pointer-events:none;cursor:default}.mdc-deprecated-list--dense ::slotted(.mdc-deprecated-list-item__primary-text){display:block;margin-top:0;line-height:normal;margin-bottom:-20px}.mdc-deprecated-list--dense ::slotted(.mdc-deprecated-list-item__primary-text)::before{display:inline-block;width:0;height:24px;content:"";vertical-align:0}.mdc-deprecated-list--dense ::slotted(.mdc-deprecated-list-item__primary-text)::after{display:inline-block;width:0;height:20px;content:"";vertical-align:-20px}`;let ti=class extends Jt{};ti.styles=[ei],ti=i([p("mwc-list")],ti);var ii,ni,oi={ANCHOR:"mdc-menu-surface--anchor",ANIMATING_CLOSED:"mdc-menu-surface--animating-closed",ANIMATING_OPEN:"mdc-menu-surface--animating-open",FIXED:"mdc-menu-surface--fixed",IS_OPEN_BELOW:"mdc-menu-surface--is-open-below",OPEN:"mdc-menu-surface--open",ROOT:"mdc-menu-surface"},si={CLOSED_EVENT:"MDCMenuSurface:closed",CLOSING_EVENT:"MDCMenuSurface:closing",OPENED_EVENT:"MDCMenuSurface:opened",FOCUSABLE_ELEMENTS:["button:not(:disabled)",'[href]:not([aria-disabled="true"])',"input:not(:disabled)","select:not(:disabled)","textarea:not(:disabled)",'[tabindex]:not([tabindex="-1"]):not([aria-disabled="true"])'].join(", ")},ai={TRANSITION_OPEN_DURATION:120,TRANSITION_CLOSE_DURATION:75,MARGIN_TO_EDGE:32,ANCHOR_TO_MENU_SURFACE_WIDTH_RATIO:.67,TOUCH_EVENT_WAIT_MS:30};!function(e){e[e.BOTTOM=1]="BOTTOM",e[e.CENTER=2]="CENTER",e[e.RIGHT=4]="RIGHT",e[e.FLIP_RTL=8]="FLIP_RTL"}(ii||(ii={})),function(e){e[e.TOP_LEFT=0]="TOP_LEFT",e[e.TOP_RIGHT=4]="TOP_RIGHT",e[e.BOTTOM_LEFT=1]="BOTTOM_LEFT",e[e.BOTTOM_RIGHT=5]="BOTTOM_RIGHT",e[e.TOP_START=8]="TOP_START",e[e.TOP_END=12]="TOP_END",e[e.BOTTOM_START=9]="BOTTOM_START",e[e.BOTTOM_END=13]="BOTTOM_END"}(ni||(ni={}));var ri=function(e){function t(i){var n=e.call(this,K(K({},t.defaultAdapter),i))||this;return n.isSurfaceOpen=!1,n.isQuickOpen=!1,n.isHoistedElement=!1,n.isFixedPosition=!1,n.isHorizontallyCenteredOnViewport=!1,n.maxHeight=0,n.openBottomBias=0,n.openAnimationEndTimerId=0,n.closeAnimationEndTimerId=0,n.animationRequestId=0,n.anchorCorner=ni.TOP_START,n.originCorner=ni.TOP_START,n.anchorMargin={top:0,right:0,bottom:0,left:0},n.position={x:0,y:0},n}return U(t,e),Object.defineProperty(t,"cssClasses",{get:function(){return oi},enumerable:!1,configurable:!0}),Object.defineProperty(t,"strings",{get:function(){return si},enumerable:!1,configurable:!0}),Object.defineProperty(t,"numbers",{get:function(){return ai},enumerable:!1,configurable:!0}),Object.defineProperty(t,"Corner",{get:function(){return ni},enumerable:!1,configurable:!0}),Object.defineProperty(t,"defaultAdapter",{get:function(){return{addClass:function(){},removeClass:function(){},hasClass:function(){return!1},hasAnchor:function(){return!1},isElementInContainer:function(){return!1},isFocused:function(){return!1},isRtl:function(){return!1},getInnerDimensions:function(){return{height:0,width:0}},getAnchorDimensions:function(){return null},getWindowDimensions:function(){return{height:0,width:0}},getBodyDimensions:function(){return{height:0,width:0}},getWindowScroll:function(){return{x:0,y:0}},setPosition:function(){},setMaxHeight:function(){},setTransformOrigin:function(){},saveFocus:function(){},restoreFocus:function(){},notifyClose:function(){},notifyOpen:function(){},notifyClosing:function(){}}},enumerable:!1,configurable:!0}),t.prototype.init=function(){var e=t.cssClasses,i=e.ROOT,n=e.OPEN;if(!this.adapter.hasClass(i))throw new Error(i+" class required in root element.");this.adapter.hasClass(n)&&(this.isSurfaceOpen=!0)},t.prototype.destroy=function(){clearTimeout(this.openAnimationEndTimerId),clearTimeout(this.closeAnimationEndTimerId),cancelAnimationFrame(this.animationRequestId)},t.prototype.setAnchorCorner=function(e){this.anchorCorner=e},t.prototype.flipCornerHorizontally=function(){this.originCorner=this.originCorner^ii.RIGHT},t.prototype.setAnchorMargin=function(e){this.anchorMargin.top=e.top||0,this.anchorMargin.right=e.right||0,this.anchorMargin.bottom=e.bottom||0,this.anchorMargin.left=e.left||0},t.prototype.setIsHoisted=function(e){this.isHoistedElement=e},t.prototype.setFixedPosition=function(e){this.isFixedPosition=e},t.prototype.isFixed=function(){return this.isFixedPosition},t.prototype.setAbsolutePosition=function(e,t){this.position.x=this.isFinite(e)?e:0,this.position.y=this.isFinite(t)?t:0},t.prototype.setIsHorizontallyCenteredOnViewport=function(e){this.isHorizontallyCenteredOnViewport=e},t.prototype.setQuickOpen=function(e){this.isQuickOpen=e},t.prototype.setMaxHeight=function(e){this.maxHeight=e},t.prototype.setOpenBottomBias=function(e){this.openBottomBias=e},t.prototype.isOpen=function(){return this.isSurfaceOpen},t.prototype.open=function(){var e=this;this.isSurfaceOpen||(this.adapter.saveFocus(),this.isQuickOpen?(this.isSurfaceOpen=!0,this.adapter.addClass(t.cssClasses.OPEN),this.dimensions=this.adapter.getInnerDimensions(),this.autoposition(),this.adapter.notifyOpen()):(this.adapter.addClass(t.cssClasses.ANIMATING_OPEN),this.animationRequestId=requestAnimationFrame((function(){e.dimensions=e.adapter.getInnerDimensions(),e.autoposition(),e.adapter.addClass(t.cssClasses.OPEN),e.openAnimationEndTimerId=setTimeout((function(){e.openAnimationEndTimerId=0,e.adapter.removeClass(t.cssClasses.ANIMATING_OPEN),e.adapter.notifyOpen()}),ai.TRANSITION_OPEN_DURATION)})),this.isSurfaceOpen=!0))},t.prototype.close=function(e){var i=this;if(void 0===e&&(e=!1),this.isSurfaceOpen){if(this.adapter.notifyClosing(),this.isQuickOpen)return this.isSurfaceOpen=!1,e||this.maybeRestoreFocus(),this.adapter.removeClass(t.cssClasses.OPEN),this.adapter.removeClass(t.cssClasses.IS_OPEN_BELOW),void this.adapter.notifyClose();this.adapter.addClass(t.cssClasses.ANIMATING_CLOSED),requestAnimationFrame((function(){i.adapter.removeClass(t.cssClasses.OPEN),i.adapter.removeClass(t.cssClasses.IS_OPEN_BELOW),i.closeAnimationEndTimerId=setTimeout((function(){i.closeAnimationEndTimerId=0,i.adapter.removeClass(t.cssClasses.ANIMATING_CLOSED),i.adapter.notifyClose()}),ai.TRANSITION_CLOSE_DURATION)})),this.isSurfaceOpen=!1,e||this.maybeRestoreFocus()}},t.prototype.handleBodyClick=function(e){var t=e.target;this.adapter.isElementInContainer(t)||this.close()},t.prototype.handleKeydown=function(e){var t=e.keyCode;("Escape"===e.key||27===t)&&this.close()},t.prototype.autoposition=function(){var e;this.measurements=this.getAutoLayoutmeasurements();var i=this.getoriginCorner(),n=this.getMenuSurfaceMaxHeight(i),o=this.hasBit(i,ii.BOTTOM)?"bottom":"top",s=this.hasBit(i,ii.RIGHT)?"right":"left",a=this.getHorizontalOriginOffset(i),r=this.getVerticalOriginOffset(i),c=this.measurements,l=c.anchorSize,d=c.surfaceSize,h=((e={})[s]=a,e[o]=r,e);l.width/d.width>ai.ANCHOR_TO_MENU_SURFACE_WIDTH_RATIO&&(s="center"),(this.isHoistedElement||this.isFixedPosition)&&this.adjustPositionForHoistedElement(h),this.adapter.setTransformOrigin(s+" "+o),this.adapter.setPosition(h),this.adapter.setMaxHeight(n?n+"px":""),this.hasBit(i,ii.BOTTOM)||this.adapter.addClass(t.cssClasses.IS_OPEN_BELOW)},t.prototype.getAutoLayoutmeasurements=function(){var e=this.adapter.getAnchorDimensions(),t=this.adapter.getBodyDimensions(),i=this.adapter.getWindowDimensions(),n=this.adapter.getWindowScroll();return e||(e={top:this.position.y,right:this.position.x,bottom:this.position.y,left:this.position.x,width:0,height:0}),{anchorSize:e,bodySize:t,surfaceSize:this.dimensions,viewportDistance:{top:e.top,right:i.width-e.right,bottom:i.height-e.bottom,left:e.left},viewportSize:i,windowScroll:n}},t.prototype.getoriginCorner=function(){var e,i,n=this.originCorner,o=this.measurements,s=o.viewportDistance,a=o.anchorSize,r=o.surfaceSize,c=t.numbers.MARGIN_TO_EDGE;this.hasBit(this.anchorCorner,ii.BOTTOM)?(e=s.top-c+this.anchorMargin.bottom,i=s.bottom-c-this.anchorMargin.bottom):(e=s.top-c+this.anchorMargin.top,i=s.bottom-c+a.height-this.anchorMargin.top),!(i-r.height>0)&&e>i+this.openBottomBias&&(n=this.setBit(n,ii.BOTTOM));var l,d,h=this.adapter.isRtl(),p=this.hasBit(this.anchorCorner,ii.FLIP_RTL),u=this.hasBit(this.anchorCorner,ii.RIGHT)||this.hasBit(n,ii.RIGHT),m=!1;(m=h&&p?!u:u)?(l=s.left+a.width+this.anchorMargin.right,d=s.right-this.anchorMargin.right):(l=s.left+this.anchorMargin.left,d=s.right+a.width-this.anchorMargin.left);var _=l-r.width>0,b=d-r.width>0,f=this.hasBit(n,ii.FLIP_RTL)&&this.hasBit(n,ii.RIGHT);return b&&f&&h||!_&&f?n=this.unsetBit(n,ii.RIGHT):(_&&m&&h||_&&!m&&u||!b&&l>=d)&&(n=this.setBit(n,ii.RIGHT)),n},t.prototype.getMenuSurfaceMaxHeight=function(e){if(this.maxHeight>0)return this.maxHeight;var i=this.measurements.viewportDistance,n=0,o=this.hasBit(e,ii.BOTTOM),s=this.hasBit(this.anchorCorner,ii.BOTTOM),a=t.numbers.MARGIN_TO_EDGE;return o?(n=i.top+this.anchorMargin.top-a,s||(n+=this.measurements.anchorSize.height)):(n=i.bottom-this.anchorMargin.bottom+this.measurements.anchorSize.height-a,s&&(n-=this.measurements.anchorSize.height)),n},t.prototype.getHorizontalOriginOffset=function(e){var t=this.measurements.anchorSize,i=this.hasBit(e,ii.RIGHT),n=this.hasBit(this.anchorCorner,ii.RIGHT);if(i){var o=n?t.width-this.anchorMargin.left:this.anchorMargin.right;return this.isHoistedElement||this.isFixedPosition?o-(this.measurements.viewportSize.width-this.measurements.bodySize.width):o}return n?t.width-this.anchorMargin.right:this.anchorMargin.left},t.prototype.getVerticalOriginOffset=function(e){var t=this.measurements.anchorSize,i=this.hasBit(e,ii.BOTTOM),n=this.hasBit(this.anchorCorner,ii.BOTTOM);return i?n?t.height-this.anchorMargin.top:-this.anchorMargin.bottom:n?t.height+this.anchorMargin.bottom:this.anchorMargin.top},t.prototype.adjustPositionForHoistedElement=function(e){var t,i,n=this.measurements,o=n.windowScroll,s=n.viewportDistance,a=n.surfaceSize,r=n.viewportSize,c=Object.keys(e);try{for(var l=W(c),d=l.next();!d.done;d=l.next()){var h=d.value,p=e[h]||0;!this.isHorizontallyCenteredOnViewport||"left"!==h&&"right"!==h?(p+=s[h],this.isFixedPosition||("top"===h?p+=o.y:"bottom"===h?p-=o.y:"left"===h?p+=o.x:p-=o.x),e[h]=p):e[h]=(r.width-a.width)/2}}catch(e){t={error:e}}finally{try{d&&!d.done&&(i=l.return)&&i.call(l)}finally{if(t)throw t.error}}},t.prototype.maybeRestoreFocus=function(){var e=this,t=this.adapter.isFocused(),i=document.activeElement&&this.adapter.isElementInContainer(document.activeElement);(t||i)&&setTimeout((function(){e.adapter.restoreFocus()}),ai.TOUCH_EVENT_WAIT_MS)},t.prototype.hasBit=function(e,t){return Boolean(e&t)},t.prototype.setBit=function(e,t){return e|t},t.prototype.unsetBit=function(e,t){return e^t},t.prototype.isFinite=function(e){return"number"==typeof e&&isFinite(e)},t}(P),ci=ri;const li={TOP_LEFT:ni.TOP_LEFT,TOP_RIGHT:ni.TOP_RIGHT,BOTTOM_LEFT:ni.BOTTOM_LEFT,BOTTOM_RIGHT:ni.BOTTOM_RIGHT,TOP_START:ni.TOP_START,TOP_END:ni.TOP_END,BOTTOM_START:ni.BOTTOM_START,BOTTOM_END:ni.BOTTOM_END};class di extends T{constructor(){super(...arguments),this.mdcFoundationClass=ci,this.absolute=!1,this.fullwidth=!1,this.fixed=!1,this.x=null,this.y=null,this.quick=!1,this.open=!1,this.stayOpenOnBodyClick=!1,this.bitwiseCorner=ni.TOP_START,this.previousMenuCorner=null,this.menuCorner="START",this.corner="TOP_START",this.styleTop="",this.styleLeft="",this.styleRight="",this.styleBottom="",this.styleMaxHeight="",this.styleTransformOrigin="",this.anchor=null,this.previouslyFocused=null,this.previousAnchor=null,this.onBodyClickBound=()=>{}}render(){const e={"mdc-menu-surface--fixed":this.fixed,"mdc-menu-surface--fullwidth":this.fullwidth},t={top:this.styleTop,left:this.styleLeft,right:this.styleRight,bottom:this.styleBottom,"max-height":this.styleMaxHeight,"transform-origin":this.styleTransformOrigin};return l`
      <div
          class="mdc-menu-surface ${d(e)}"
          style="${M(t)}"
          @keydown=${this.onKeydown}
          @opened=${this.registerBodyClick}
          @closed=${this.deregisterBodyClick}>
        <slot></slot>
      </div>`}createAdapter(){return Object.assign(Object.assign({},G(this.mdcRoot)),{hasAnchor:()=>!!this.anchor,notifyClose:()=>{const e=new CustomEvent("closed",{bubbles:!0,composed:!0});this.open=!1,this.mdcRoot.dispatchEvent(e)},notifyClosing:()=>{const e=new CustomEvent("closing",{bubbles:!0,composed:!0});this.mdcRoot.dispatchEvent(e)},notifyOpen:()=>{const e=new CustomEvent("opened",{bubbles:!0,composed:!0});this.open=!0,this.mdcRoot.dispatchEvent(e)},isElementInContainer:()=>!1,isRtl:()=>!!this.mdcRoot&&"rtl"===getComputedStyle(this.mdcRoot).direction,setTransformOrigin:e=>{this.mdcRoot&&(this.styleTransformOrigin=e)},isFocused:()=>H(this),saveFocus:()=>{const e=V(),t=e.length;t||(this.previouslyFocused=null),this.previouslyFocused=e[t-1]},restoreFocus:()=>{this.previouslyFocused&&"focus"in this.previouslyFocused&&this.previouslyFocused.focus()},getInnerDimensions:()=>{const e=this.mdcRoot;return e?{width:e.offsetWidth,height:e.offsetHeight}:{width:0,height:0}},getAnchorDimensions:()=>{const e=this.anchor;return e?e.getBoundingClientRect():null},getBodyDimensions:()=>({width:document.body.clientWidth,height:document.body.clientHeight}),getWindowDimensions:()=>({width:window.innerWidth,height:window.innerHeight}),getWindowScroll:()=>({x:window.pageXOffset,y:window.pageYOffset}),setPosition:e=>{this.mdcRoot&&(this.styleLeft="left"in e?e.left+"px":"",this.styleRight="right"in e?e.right+"px":"",this.styleTop="top"in e?e.top+"px":"",this.styleBottom="bottom"in e?e.bottom+"px":"")},setMaxHeight:async e=>{this.mdcRoot&&(this.styleMaxHeight=e,await this.updateComplete,this.styleMaxHeight=`var(--mdc-menu-max-height, ${e})`)}})}onKeydown(e){this.mdcFoundation&&this.mdcFoundation.handleKeydown(e)}onBodyClick(e){if(this.stayOpenOnBodyClick)return;-1===e.composedPath().indexOf(this)&&this.close()}registerBodyClick(){this.onBodyClickBound=this.onBodyClick.bind(this),document.body.addEventListener("click",this.onBodyClickBound,{passive:!0,capture:!0})}deregisterBodyClick(){document.body.removeEventListener("click",this.onBodyClickBound,{capture:!0})}close(){this.open=!1}show(){this.open=!0}}i([n(".mdc-menu-surface")],di.prototype,"mdcRoot",void 0),i([n("slot")],di.prototype,"slotElement",void 0),i([s({type:Boolean}),q((function(e){this.mdcFoundation&&!this.fixed&&this.mdcFoundation.setIsHoisted(e)}))],di.prototype,"absolute",void 0),i([s({type:Boolean})],di.prototype,"fullwidth",void 0),i([s({type:Boolean}),q((function(e){this.mdcFoundation&&!this.absolute&&this.mdcFoundation.setFixedPosition(e)}))],di.prototype,"fixed",void 0),i([s({type:Number}),q((function(e){this.mdcFoundation&&null!==this.y&&null!==e&&(this.mdcFoundation.setAbsolutePosition(e,this.y),this.mdcFoundation.setAnchorMargin({left:e,top:this.y,right:-e,bottom:this.y}))}))],di.prototype,"x",void 0),i([s({type:Number}),q((function(e){this.mdcFoundation&&null!==this.x&&null!==e&&(this.mdcFoundation.setAbsolutePosition(this.x,e),this.mdcFoundation.setAnchorMargin({left:this.x,top:e,right:-this.x,bottom:e}))}))],di.prototype,"y",void 0),i([s({type:Boolean}),q((function(e){this.mdcFoundation&&this.mdcFoundation.setQuickOpen(e)}))],di.prototype,"quick",void 0),i([s({type:Boolean,reflect:!0}),q((function(e,t){this.mdcFoundation&&(e?this.mdcFoundation.open():void 0!==t&&this.mdcFoundation.close())}))],di.prototype,"open",void 0),i([s({type:Boolean})],di.prototype,"stayOpenOnBodyClick",void 0),i([a(),q((function(e){this.mdcFoundation&&this.mdcFoundation.setAnchorCorner(e)}))],di.prototype,"bitwiseCorner",void 0),i([s({type:String}),q((function(e){if(this.mdcFoundation){const t="START"===e||"END"===e,i=null===this.previousMenuCorner,n=!i&&e!==this.previousMenuCorner,o=i&&"END"===e;t&&(n||o)&&(this.bitwiseCorner=this.bitwiseCorner^ii.RIGHT,this.mdcFoundation.flipCornerHorizontally(),this.previousMenuCorner=e)}}))],di.prototype,"menuCorner",void 0),i([s({type:String}),q((function(e){if(this.mdcFoundation&&e){let t=li[e];"END"===this.menuCorner&&(t^=ii.RIGHT),this.bitwiseCorner=t}}))],di.prototype,"corner",void 0),i([a()],di.prototype,"styleTop",void 0),i([a()],di.prototype,"styleLeft",void 0),i([a()],di.prototype,"styleRight",void 0),i([a()],di.prototype,"styleBottom",void 0),i([a()],di.prototype,"styleMaxHeight",void 0),i([a()],di.prototype,"styleTransformOrigin",void 0);const hi=h`.mdc-menu-surface{display:none;position:absolute;box-sizing:border-box;max-width:calc(100vw - 32px);max-width:var(--mdc-menu-max-width, calc(100vw - 32px));max-height:calc(100vh - 32px);max-height:var(--mdc-menu-max-height, calc(100vh - 32px));margin:0;padding:0;transform:scale(1);transform-origin:top left;opacity:0;overflow:auto;will-change:transform,opacity;z-index:8;transition:opacity .03s linear,transform .12s cubic-bezier(0, 0, 0.2, 1),height 250ms cubic-bezier(0, 0, 0.2, 1);box-shadow:0px 5px 5px -3px rgba(0, 0, 0, 0.2),0px 8px 10px 1px rgba(0, 0, 0, 0.14),0px 3px 14px 2px rgba(0,0,0,.12);background-color:#fff;background-color:var(--mdc-theme-surface, #fff);color:#000;color:var(--mdc-theme-on-surface, #000);border-radius:4px;border-radius:var(--mdc-shape-medium, 4px);transform-origin-left:top left;transform-origin-right:top right}.mdc-menu-surface:focus{outline:none}.mdc-menu-surface--animating-open{display:inline-block;transform:scale(0.8);opacity:0}.mdc-menu-surface--open{display:inline-block;transform:scale(1);opacity:1}.mdc-menu-surface--animating-closed{display:inline-block;opacity:0;transition:opacity .075s linear}[dir=rtl] .mdc-menu-surface,.mdc-menu-surface[dir=rtl]{transform-origin-left:top right;transform-origin-right:top left}.mdc-menu-surface--anchor{position:relative;overflow:visible}.mdc-menu-surface--fixed{position:fixed}.mdc-menu-surface--fullwidth{width:100%}:host(:not([open])){display:none}.mdc-menu-surface{z-index:8;z-index:var(--mdc-menu-z-index, 8);min-width:112px;min-width:var(--mdc-menu-min-width, 112px)}`;let pi=class extends di{};pi.styles=[hi],pi=i([p("mwc-menu-surface")],pi);var ui,mi={MENU_SELECTED_LIST_ITEM:"mdc-menu-item--selected",MENU_SELECTION_GROUP:"mdc-menu__selection-group",ROOT:"mdc-menu"},_i={ARIA_CHECKED_ATTR:"aria-checked",ARIA_DISABLED_ATTR:"aria-disabled",CHECKBOX_SELECTOR:'input[type="checkbox"]',LIST_SELECTOR:".mdc-list,.mdc-deprecated-list",SELECTED_EVENT:"MDCMenu:selected",SKIP_RESTORE_FOCUS:"data-menu-item-skip-restore-focus"},bi={FOCUS_ROOT_INDEX:-1};!function(e){e[e.NONE=0]="NONE",e[e.LIST_ROOT=1]="LIST_ROOT",e[e.FIRST_ITEM=2]="FIRST_ITEM",e[e.LAST_ITEM=3]="LAST_ITEM"}(ui||(ui={}));var fi=function(e){function t(i){var n=e.call(this,K(K({},t.defaultAdapter),i))||this;return n.closeAnimationEndTimerId=0,n.defaultFocusState=ui.LIST_ROOT,n.selectedIndex=-1,n}return U(t,e),Object.defineProperty(t,"cssClasses",{get:function(){return mi},enumerable:!1,configurable:!0}),Object.defineProperty(t,"strings",{get:function(){return _i},enumerable:!1,configurable:!0}),Object.defineProperty(t,"numbers",{get:function(){return bi},enumerable:!1,configurable:!0}),Object.defineProperty(t,"defaultAdapter",{get:function(){return{addClassToElementAtIndex:function(){},removeClassFromElementAtIndex:function(){},addAttributeToElementAtIndex:function(){},removeAttributeFromElementAtIndex:function(){},getAttributeFromElementAtIndex:function(){return null},elementContainsClass:function(){return!1},closeSurface:function(){},getElementIndex:function(){return-1},notifySelected:function(){},getMenuItemCount:function(){return 0},focusItemAtIndex:function(){},focusListRoot:function(){},getSelectedSiblingOfItemAtIndex:function(){return-1},isSelectableItemAtIndex:function(){return!1}}},enumerable:!1,configurable:!0}),t.prototype.destroy=function(){this.closeAnimationEndTimerId&&clearTimeout(this.closeAnimationEndTimerId),this.adapter.closeSurface()},t.prototype.handleKeydown=function(e){var t=e.key,i=e.keyCode;("Tab"===t||9===i)&&this.adapter.closeSurface(!0)},t.prototype.handleItemAction=function(e){var t=this,i=this.adapter.getElementIndex(e);if(!(i<0)){this.adapter.notifySelected({index:i});var n="true"===this.adapter.getAttributeFromElementAtIndex(i,_i.SKIP_RESTORE_FOCUS);this.adapter.closeSurface(n),this.closeAnimationEndTimerId=setTimeout((function(){var i=t.adapter.getElementIndex(e);i>=0&&t.adapter.isSelectableItemAtIndex(i)&&t.setSelectedIndex(i)}),ri.numbers.TRANSITION_CLOSE_DURATION)}},t.prototype.handleMenuSurfaceOpened=function(){switch(this.defaultFocusState){case ui.FIRST_ITEM:this.adapter.focusItemAtIndex(0);break;case ui.LAST_ITEM:this.adapter.focusItemAtIndex(this.adapter.getMenuItemCount()-1);break;case ui.NONE:break;default:this.adapter.focusListRoot()}},t.prototype.setDefaultFocusState=function(e){this.defaultFocusState=e},t.prototype.getSelectedIndex=function(){return this.selectedIndex},t.prototype.setSelectedIndex=function(e){if(this.validatedIndex(e),!this.adapter.isSelectableItemAtIndex(e))throw new Error("MDCMenuFoundation: No selection group at specified index.");var t=this.adapter.getSelectedSiblingOfItemAtIndex(e);t>=0&&(this.adapter.removeAttributeFromElementAtIndex(t,_i.ARIA_CHECKED_ATTR),this.adapter.removeClassFromElementAtIndex(t,mi.MENU_SELECTED_LIST_ITEM)),this.adapter.addClassToElementAtIndex(e,mi.MENU_SELECTED_LIST_ITEM),this.adapter.addAttributeToElementAtIndex(e,_i.ARIA_CHECKED_ATTR,"true"),this.selectedIndex=e},t.prototype.setEnabled=function(e,t){this.validatedIndex(e),t?(this.adapter.removeClassFromElementAtIndex(e,$t),this.adapter.addAttributeToElementAtIndex(e,_i.ARIA_DISABLED_ATTR,"false")):(this.adapter.addClassToElementAtIndex(e,$t),this.adapter.addAttributeToElementAtIndex(e,_i.ARIA_DISABLED_ATTR,"true"))},t.prototype.validatedIndex=function(e){var t=this.adapter.getMenuItemCount();if(!(e>=0&&e<t))throw new Error("MDCMenuFoundation: No list item at specified index.")},t}(P);class gi extends T{constructor(){super(...arguments),this.mdcFoundationClass=fi,this.listElement_=null,this.anchor=null,this.open=!1,this.quick=!1,this.wrapFocus=!1,this.innerRole="menu",this.innerAriaLabel=null,this.corner="TOP_START",this.x=null,this.y=null,this.absolute=!1,this.multi=!1,this.activatable=!1,this.fixed=!1,this.forceGroupSelection=!1,this.fullwidth=!1,this.menuCorner="START",this.stayOpenOnBodyClick=!1,this.defaultFocus="LIST_ROOT",this._listUpdateComplete=null}get listElement(){return this.listElement_||(this.listElement_=this.renderRoot.querySelector("mwc-list")),this.listElement_}get items(){const e=this.listElement;return e?e.items:[]}get index(){const e=this.listElement;return e?e.index:-1}get selected(){const e=this.listElement;return e?e.selected:null}render(){const e="menu"===this.innerRole?"menuitem":"option";return l`
      <mwc-menu-surface
          ?hidden=${!this.open}
          .anchor=${this.anchor}
          .open=${this.open}
          .quick=${this.quick}
          .corner=${this.corner}
          .x=${this.x}
          .y=${this.y}
          .absolute=${this.absolute}
          .fixed=${this.fixed}
          .fullwidth=${this.fullwidth}
          .menuCorner=${this.menuCorner}
          ?stayOpenOnBodyClick=${this.stayOpenOnBodyClick}
          class="mdc-menu mdc-menu-surface"
          @closed=${this.onClosed}
          @opened=${this.onOpened}
          @keydown=${this.onKeydown}>
        <mwc-list
          rootTabbable
          .innerAriaLabel=${this.innerAriaLabel}
          .innerRole=${this.innerRole}
          .multi=${this.multi}
          class="mdc-deprecated-list"
          .itemRoles=${e}
          .wrapFocus=${this.wrapFocus}
          .activatable=${this.activatable}
          @action=${this.onAction}>
        <slot></slot>
      </mwc-list>
    </mwc-menu-surface>`}createAdapter(){return{addClassToElementAtIndex:(e,t)=>{const i=this.listElement;if(!i)return;const n=i.items[e];n&&("mdc-menu-item--selected"===t?this.forceGroupSelection&&!n.selected&&i.toggle(e,!0):n.classList.add(t))},removeClassFromElementAtIndex:(e,t)=>{const i=this.listElement;if(!i)return;const n=i.items[e];n&&("mdc-menu-item--selected"===t?n.selected&&i.toggle(e,!1):n.classList.remove(t))},addAttributeToElementAtIndex:(e,t,i)=>{const n=this.listElement;if(!n)return;const o=n.items[e];o&&o.setAttribute(t,i)},removeAttributeFromElementAtIndex:(e,t)=>{const i=this.listElement;if(!i)return;const n=i.items[e];n&&n.removeAttribute(t)},getAttributeFromElementAtIndex:(e,t)=>{const i=this.listElement;if(!i)return null;const n=i.items[e];return n?n.getAttribute(t):null},elementContainsClass:(e,t)=>e.classList.contains(t),closeSurface:()=>{this.open=!1},getElementIndex:e=>{const t=this.listElement;return t?t.items.indexOf(e):-1},notifySelected:()=>{},getMenuItemCount:()=>{const e=this.listElement;return e?e.items.length:0},focusItemAtIndex:e=>{const t=this.listElement;if(!t)return;const i=t.items[e];i&&i.focus()},focusListRoot:()=>{this.listElement&&this.listElement.focus()},getSelectedSiblingOfItemAtIndex:e=>{const t=this.listElement;if(!t)return-1;const i=t.items[e];if(!i||!i.group)return-1;for(let n=0;n<t.items.length;n++){if(n===e)continue;const o=t.items[n];if(o.selected&&o.group===i.group)return n}return-1},isSelectableItemAtIndex:e=>{const t=this.listElement;if(!t)return!1;const i=t.items[e];return!!i&&i.hasAttribute("group")}}}onKeydown(e){this.mdcFoundation&&this.mdcFoundation.handleKeydown(e)}onAction(e){const t=this.listElement;if(this.mdcFoundation&&t){const i=e.detail.index,n=t.items[i];n&&this.mdcFoundation.handleItemAction(n)}}onOpened(){this.open=!0,this.mdcFoundation&&this.mdcFoundation.handleMenuSurfaceOpened()}onClosed(){this.open=!1}async getUpdateComplete(){await this._listUpdateComplete;return await super.getUpdateComplete()}async firstUpdated(){super.firstUpdated();const e=this.listElement;e&&(this._listUpdateComplete=e.updateComplete,await this._listUpdateComplete)}select(e){const t=this.listElement;t&&t.select(e)}close(){this.open=!1}show(){this.open=!0}getFocusedItemIndex(){const e=this.listElement;return e?e.getFocusedItemIndex():-1}focusItemAtIndex(e){const t=this.listElement;t&&t.focusItemAtIndex(e)}layout(e=!0){const t=this.listElement;t&&t.layout(e)}}i([n(".mdc-menu")],gi.prototype,"mdcRoot",void 0),i([n("slot")],gi.prototype,"slotElement",void 0),i([s({type:Object})],gi.prototype,"anchor",void 0),i([s({type:Boolean,reflect:!0})],gi.prototype,"open",void 0),i([s({type:Boolean})],gi.prototype,"quick",void 0),i([s({type:Boolean})],gi.prototype,"wrapFocus",void 0),i([s({type:String})],gi.prototype,"innerRole",void 0),i([s({type:String})],gi.prototype,"innerAriaLabel",void 0),i([s({type:String})],gi.prototype,"corner",void 0),i([s({type:Number})],gi.prototype,"x",void 0),i([s({type:Number})],gi.prototype,"y",void 0),i([s({type:Boolean})],gi.prototype,"absolute",void 0),i([s({type:Boolean})],gi.prototype,"multi",void 0),i([s({type:Boolean})],gi.prototype,"activatable",void 0),i([s({type:Boolean})],gi.prototype,"fixed",void 0),i([s({type:Boolean})],gi.prototype,"forceGroupSelection",void 0),i([s({type:Boolean})],gi.prototype,"fullwidth",void 0),i([s({type:String})],gi.prototype,"menuCorner",void 0),i([s({type:Boolean})],gi.prototype,"stayOpenOnBodyClick",void 0),i([s({type:String}),q((function(e){this.mdcFoundation&&this.mdcFoundation.setDefaultFocusState(ui[e])}))],gi.prototype,"defaultFocus",void 0);const vi=h`mwc-list ::slotted([mwc-list-item]:not([twoline])),mwc-list ::slotted([noninteractive]:not([twoline])){height:var(--mdc-menu-item-height, 48px)}`;let yi=class extends gi{};yi.styles=[vi],yi=i([p("mwc-menu")],yi),E([p("ha-button-menu")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[s()],key:"corner",value:()=>"TOP_START"},{kind:"field",decorators:[s({type:Boolean})],key:"multi",value:()=>!1},{kind:"field",decorators:[s({type:Boolean})],key:"activatable",value:()=>!1},{kind:"field",decorators:[s({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[s({type:Boolean})],key:"fixed",value:()=>!1},{kind:"field",decorators:[n("mwc-menu",!0)],key:"_menu",value:void 0},{kind:"get",key:"items",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.items}},{kind:"get",key:"selected",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.selected}},{kind:"method",key:"render",value:function(){return l`
      <div @click=${this._handleClick}>
        <slot name="trigger"></slot>
      </div>
      <mwc-menu
        .corner=${this.corner}
        .fixed=${this.fixed}
        .multi=${this.multi}
        .activatable=${this.activatable}
      >
        <slot></slot>
      </mwc-menu>
    `}},{kind:"method",key:"_handleClick",value:function(){this.disabled||(this._menu.anchor=this,this._menu.show())}},{kind:"get",static:!0,key:"styles",value:function(){return h`
      :host {
        display: inline-block;
        position: relative;
      }
      ::slotted([disabled]) {
        color: var(--disabled-text-color);
      }
    `}}]}}),r);const xi=(e,t)=>e.callWS({type:"insteon/device/get",device_id:t}),ki=(e,t)=>e.callWS({type:"insteon/aldb/get",device_address:t}),wi=(e,t,i)=>e.callWS({type:"insteon/properties/get",device_address:t,show_advanced:i}),Ei=(e,t,i)=>e.callWS({type:"insteon/aldb/change",device_address:t,record:i}),Ii=(e,t,i,n)=>e.callWS({type:"insteon/properties/change",device_address:t,name:i,value:n}),Ci=(e,t,i)=>e.callWS({type:"insteon/device/add",device_address:t,multiple:i}),Si=e=>e.callWS({type:"insteon/device/add/cancel"}),Ti=(e,t,i)=>e.callWS({type:"insteon/aldb/create",device_address:t,record:i}),Ai=(e,t)=>e.callWS({type:"insteon/aldb/load",device_address:t}),Ri=(e,t)=>e.callWS({type:"insteon/properties/load",device_address:t}),Oi=(e,t)=>e.callWS({type:"insteon/aldb/write",device_address:t}),Fi=(e,t)=>e.callWS({type:"insteon/properties/write",device_address:t}),zi=(e,t)=>e.callWS({type:"insteon/aldb/reset",device_address:t}),Mi=(e,t)=>e.callWS({type:"insteon/properties/reset",device_address:t}),Li=(e,t)=>e.callWS({type:"insteon/aldb/add_default_links",device_address:t}),Di=e=>[{name:"mode",options:[["c",e.localize("aldb.mode.controller")],["r",e.localize("aldb.mode.responder")]],required:!0,type:"select"},{name:"group",required:!0,type:"integer",valueMin:-1,valueMax:255},{name:"target",required:!0,type:"string"},{name:"data1",required:!0,type:"integer",valueMin:-1,valueMax:255},{name:"data2",required:!0,type:"integer",valueMin:-1,valueMax:255},{name:"data3",required:!0,type:"integer",valueMin:-1,valueMax:255}],Bi=e=>[{name:"in_use",required:!0,type:"boolean"},...Di(e)],$i=e=>[{name:"multiple",required:!0,type:"boolean"},{name:"address",required:!1,type:e?"constant":"string"}];export{De as A,Wt as B,Lt as C,ni as D,Si as E,ht as F,Pe as I,_t as K,st as P,Ci as a,it as b,Ve as c,at as d,ki as e,xi as f,Di as g,zi as h,Li as i,Ei as j,Ti as k,Ai as l,Bi as m,Ri as n,Fi as o,wi as p,Mi as q,Me as r,Ii as s,$i as t,q as u,j as v,Oi as w,J as x,oe as y,tt as z};
