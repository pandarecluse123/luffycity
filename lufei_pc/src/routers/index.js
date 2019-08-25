import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router);

import Home from "../components/Home";
import Login from "../components/Login";
import Register from "../components/Register";
import Course from "../components/Course";
import Detail from "../components/Detail";
import Cart from "../components/Cart";
import Order from "../components/Order";
import Success from "../components/Success";

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

     {name:'Detail',
    path:'/course/:course',
    component:Detail},

     {name:'Cart',
    path:'/cart',
    component:Cart},

      {name:'Order',
    path:'/order',
    component:Order},

    {name:'Success',
    path:'/pay/result',
    component:Success},
  ]
})
