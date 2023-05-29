/*
 * @Descripttion: 
 * @version: 0.x
 * @Author: zhai
 * @Date: 2023-05-27 19:59:43
 * @LastEditors: zhai
 * @LastEditTime: 2023-05-27 20:57:16
 */
import {createApp} from 'vue';
import pinia from '/@/stores/index';
import App from './App.vue';
import router from './router';
import {directive} from '/@/directive/index';
import other from '/@/utils/other';

import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import '/@/theme/index.scss';

import mqttVueHook from 'mqtt-vue-hook'


const app = createApp(App);

directive(app);
other.apiPublicAssembly(app)

const protocol = 'ws'
const host = '127.0.0.1'
const port = 8083


// app.use(mqttVueHook, options)
app.use(mqttVueHook, `${protocol}://${host}:${port}/mqtt`, {
  clean: false,
  keepalive: 60,
  clientId: `mqtt_client_${Math.random().toString(16).substring(2, 10)}`,
  connectTimeout: 4000,
})


app.use(pinia).use(router).use(ElementPlus).mount('#app');
