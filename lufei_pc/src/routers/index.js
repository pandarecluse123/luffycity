import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router);

import Home from "../components/Home";
import Login from "../components/Login";
import Register from "../components/Register";
import Course from "../components/Course";

export default new Router({
  mode:'history',
  routes:[
    {name:'Home',
    path:'/',
    component:Home},

    {name:'Login',
    path:'/user/login',
    component:Login},

    {name:'Register',
    path:'/user/register',
    component:Register},

    {name:'Course',
    path:'/course',
    component:Course},

  ]
})
