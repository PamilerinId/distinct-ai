import Vue from 'vue';
import Router from 'vue-router';
import Invoice from '../components/Invoice.vue';
import Ping from '../components/Ping.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Invoice Generator',
      component: Invoice,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
  ],
});
