/* eslint-disable */
import Vue from 'vue';
import Router from 'vue-router';
import ToDo from '../components/ToDo';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'ToDo',
      component: ToDo,
    },
  ],
});
