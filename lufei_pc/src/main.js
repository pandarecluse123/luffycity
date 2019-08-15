// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './routers/index'
import settings from "./settings"
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import axios from 'axios'; // 从node_modules目录中导入包
import '../static/js/gt'//导入极验验证码js文件

// 允许ajax发送请求时附带cookie
axios.defaults.withCredentials = true;

Vue.prototype.$axios = axios; // 把对象挂载vue中

Vue.config.productionTip = false;
Vue.prototype.$settings = settings;
Vue.use(ElementUI);

require('video.js/dist/video-js.css');
require('vue-video-player/src/custom-theme.css');
import VideoPlayer from 'vue-video-player'
Vue.use(VideoPlayer);


/* eslint-disable no-new */
new Vue({
  el: '#app',
  components: { App },
  router,
  template: '<App/>'
});

