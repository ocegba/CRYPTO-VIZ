/*! For license information please see module.js.LICENSE.txt */
define(["react","@grafana/ui","@grafana/data","@grafana/runtime","lodash"],(function(e,t,n,a,o){return function(e){var t={};function n(a){if(t[a])return t[a].exports;var o=t[a]={i:a,l:!1,exports:{}};return e[a].call(o.exports,o,o.exports,n),o.l=!0,o.exports}return n.m=e,n.c=t,n.d=function(e,t,a){n.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:a})},n.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.t=function(e,t){if(1&t&&(e=n(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var a=Object.create(null);if(n.r(a),Object.defineProperty(a,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var o in e)n.d(a,o,function(t){return e[t]}.bind(null,o));return a},n.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return n.d(t,"a",t),t},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.p="/",n(n.s=5)}([function(t,n){t.exports=e},function(e,n){e.exports=t},function(e,t){e.exports=n},function(e,t){e.exports=a},function(e,t){e.exports=o},function(e,t,n){"use strict";n.r(t);var a=n(2),o=function(e,t){return(o=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(e,t){e.__proto__=t}||function(e,t){for(var n in t)t.hasOwnProperty(n)&&(e[n]=t[n])})(e,t)};function r(e,t){function n(){this.constructor=e}o(e,t),e.prototype=null===t?Object.create(t):(n.prototype=t.prototype,new n)}var i=function(){return(i=Object.assign||function(e){for(var t,n=1,a=arguments.length;n<a;n++)for(var o in t=arguments[n])Object.prototype.hasOwnProperty.call(t,o)&&(e[o]=t[o]);return e}).apply(this,arguments)};var s,u,l=function(e){function t(t){return e.call(this,t)||this}return r(t,e),t}(n(3).DataSourceWithBackend),c=n(0),p=n.n(c),f=n(1),m=f.LegacyForms.SecretFormField,h=f.LegacyForms.FormField,d=function(e){function t(){var t=null!==e&&e.apply(this,arguments)||this;return t.onAPIKeyChange=function(e){var n=t.props,a=n.onOptionsChange,o=n.options;a(i(i({},o),{secureJsonData:{apiKey:e.target.value}}))},t.onResetAPIKey=function(){var e=t.props,n=e.onOptionsChange,a=e.options;n(i(i({},a),{secureJsonFields:i(i({},a.secureJsonFields),{apiKey:!1}),secureJsonData:i(i({},a.secureJsonData),{apiKey:""})}))},t.onBootstrapServersChange=function(e){var n=t.props,a=n.onOptionsChange,o=n.options,r=i(i({},o.jsonData),{bootstrapServers:e.target.value});a(i(i({},o),{jsonData:r}))},t}return r(t,e),t.prototype.render=function(){var e=this.props.options,t=e.jsonData,n=e.secureJsonFields,a=e.secureJsonData||{};return p.a.createElement("div",{className:"gf-form-group"},p.a.createElement("div",{className:"gf-form"},p.a.createElement(h,{label:"Servers",onChange:this.onBootstrapServersChange,value:t.bootstrapServers||"",placeholder:"broker1:9092, broker2:9092"})),p.a.createElement("div",{className:"gf-form-inline"},p.a.createElement("div",{className:"gf-form"},p.a.createElement(m,{isConfigured:n&&n.apiKey,value:a.apiKey||"",label:"API Key",placeholder:"secure json field (backend only)",labelWidth:6,inputWidth:20,onReset:this.onResetAPIKey,onChange:this.onAPIKeyChange}))))},t}(c.PureComponent),g=n(4);!function(e){e.EARLIEST="earliest",e.LATEST="latest"}(s||(s={})),function(e){e.Now="now",e.Message="message"}(u||(u={}));var v={partition:0,withStreaming:!0,autoOffsetReset:s.LATEST,timestampMode:u.Now},y=[{label:"From the last 100",value:s.EARLIEST,description:"Consume from the last 100 offset"},{label:"Latest",value:s.LATEST,description:"Consume from the latest offset"}],b=[{label:"Now",value:u.Now,description:"Current time while consuming the message"},{label:"Message Timestamp",value:u.Message,description:"The message timestamp while producing into topic"}],E=function(e){function t(){var t=null!==e&&e.apply(this,arguments)||this;return t.onTopicNameChange=function(e){var n=t.props,a=n.onChange,o=n.query,r=n.onRunQuery;a(i(i({},o),{topicName:e.target.value})),r()},t.onPartitionChange=function(e){var n=t.props,a=n.onChange,o=n.query,r=n.onRunQuery;a(i(i({},o),{partition:parseFloat(e.target.value)})),r()},t.onWithStreamingChange=function(e){var n=t.props,a=n.onChange,o=n.query,r=n.onRunQuery;a(i(i({},o),{withStreaming:e.currentTarget.checked})),r()},t.onAutoResetOffsetChanged=function(e){var n=t.props,a=n.onChange,o=n.query,r=n.onRunQuery;a(i(i({},o),{autoOffsetReset:e.value||s.LATEST})),r()},t.resolveAutoResetOffset=function(e){return e===s.LATEST?y[1]:y[0]},t.onTimestampModeChanged=function(e){var n=t.props,a=n.onChange,o=n.query,r=n.onRunQuery;a(i(i({},o),{timestampMode:e.value||u.Now})),r()},t.resolveTimestampMode=function(e){return e===u.Now?b[0]:b[1]},t}return r(t,e),t.prototype.render=function(){var e=Object(g.defaults)(this.props.query,v),t=e.topicName,n=e.partition,a=e.withStreaming,o=e.autoOffsetReset,r=e.timestampMode;return p.a.createElement(p.a.Fragment,null,p.a.createElement("div",{className:"gf-form"},p.a.createElement(f.InlineFieldRow,null,p.a.createElement(f.InlineFormLabel,{width:10},"Topic"),p.a.createElement("input",{className:"gf-form-input width-14",value:t||"",onChange:this.onTopicNameChange,type:"text"}),p.a.createElement(f.InlineFormLabel,{width:10},"Partition"),p.a.createElement("input",{className:"gf-form-input width-14",value:n,onChange:this.onPartitionChange,type:"number",step:"1",min:"0"}),p.a.createElement(f.InlineFormLabel,null,"Enable streaming ",p.a.createElement("small",null,"(v8+)")),p.a.createElement("div",{className:"add-data-source-item-badge"},p.a.createElement(f.Switch,{css:!0,checked:a||!1,onChange:this.onWithStreamingChange})))),p.a.createElement("div",{className:"gf-form"},p.a.createElement(f.InlineFieldRow,null,p.a.createElement(f.InlineFormLabel,{className:"width-5",tooltip:"Starting offset to consume that can be from latest or last 100."},"Auto offset reset"),p.a.createElement("div",{className:"gf-form--has-input-icon"},p.a.createElement(f.Select,{className:"width-14",value:this.resolveAutoResetOffset(o),options:y,defaultValue:y[0],onChange:this.onAutoResetOffsetChanged})),p.a.createElement(f.InlineFormLabel,{tooltip:"Timestamp of the kafka value to visualize."},"Timestamp Mode"),p.a.createElement("div",{className:"gf-form--has-input-icon"},p.a.createElement(f.Select,{className:"width-14",value:this.resolveTimestampMode(r),options:b,defaultValue:b[0],onChange:this.onTimestampModeChanged})))))},t}(c.PureComponent);n.d(t,"plugin",(function(){return C}));var C=new a.DataSourcePlugin(l).setConfigEditor(d).setQueryEditor(E)}])}));
//# sourceMappingURL=module.js.map