<template>
  <div class="cart">
    <Header/>
    <div class="cart-info">
        <h3 class="cart-top">购物车结算 <span>共{{course_list.length}}门课程</span></h3>
        <div class="cart-title">
           <el-row>
             <el-col :span="2">&nbsp;</el-col>
             <el-col :span="10">课程</el-col>
             <el-col :span="8">有效期</el-col>
             <el-col :span="4">价格</el-col>
           </el-row>
        </div>
        <div class="cart-item" v-for="course,key in course_list" :key="key">
          <el-row>
             <el-col :span="2" class="checkbox">&nbsp;&nbsp;</el-col>
             <el-col :span="10" class="course-info">
               <img :src="course.img" alt="">
                <div class="course_name">
                 {{course.name}}
                 <span class="discount_name">{{course.discount_name}}</span>
               </div>
             </el-col>
             <el-col :span="8"><span>{{course.expire}}</span></el-col>
            <el-col :span="4" class="course-price">
               ¥{{course.real_price}}
               <span class="original-price">原价 ¥{{course.price}}</span>
             </el-col>
           </el-row>
        </div>
        <div class="calc">
            <el-row class="pay-row">
              <el-col :span="4" class="pay-col"><span class="pay-text">支付方式：</span></el-col>
              <el-col :span="8">
                <span class="alipay" @click="pay_type=1">
                  <img v-if='pay_type==1' src="../../static/image/alipay2.png" alt="">
                  <img v-else src="../../static/image/alipay.png" alt="">
                </span>
                <span class="alipay wechat" @click="pay_type=2">
                  <img v-if="pay_type==2" src="../../static/image/wechat2.png" alt="">
                  <img v-else src="../../static/image/wechat.png" alt="">
                </span>
              </el-col>
              <el-col :span="8" class="count">实付款： <span>¥99.50</span></el-col>
              <el-col :span="4" class="cart-pay"><span>去支付</span></el-col>
            </el-row>
        </div>
    </div>
    <Footer/>
  </div>
</template>


<script>
  import Header from "./common/Header";
  import Footer from "./common/Footer";
    export default {
        name: "Order",
        data(){
          return{
              course_list:[],
              pay_type:1
          }
        },
        components:{
            Header,
            Footer
        },
        created() {
            this.get_course_list()
        },
        methods:{
            check_user(){
             let user_token=localStorage.getItem('user_token') || sessionStorage.getItem('user_token');
            if(!user_token){
                this.$confirm('对不起,请登录后继续操作','警告').then(()=>{
                     this.$router.push('/user/login/');
                });
                return false
            }
             return user_token
        },
            get_course_list(){
                 this.$axios.get(`${this.$settings.Host}/cart/course/selected_order/`, {
                headers:{
                    'Authorization':'jwt '+this.check_user()
                }
            }
          ).then(response=>{
             this.course_list=response.data
          }).catch(error=>{
              this.$message('出现问题')
          });
            }
        }
    }



</script>

<style scoped>
.cart{
  margin-top: 80px;
}
.cart-info{
  overflow: hidden;
  width: 1200px;
  margin: auto;
}
.cart-top{
  font-size: 18px;
  color: #666;
  margin: 25px 0;
  font-weight: normal;
}
.cart-top span{
    font-size: 12px;
    color: #d0d0d0;
    display: inline-block;
}
.cart-title{
    background: #F7F7F7;
    height: 70px;
}
.calc{
  margin-top: 25px;
  margin-bottom: 40px;
}

.calc .count{
  text-align: right;
  margin-right: 10px;
  vertical-align: middle;
}
.calc .count span{
    font-size: 36px;
    color: #333;
}
.calc .cart-pay{
    margin-top: 5px;
    width: 110px;
    height: 38px;
    outline: none;
    border: none;
    color: #fff;
    line-height: 38px;
    background: #ffc210;
    border-radius: 4px;
    font-size: 16px;
    text-align: center;
    cursor: pointer;
}
.cart-item{
  height: 120px;
  line-height: 120px;
  margin-bottom: 30px;
}
.course-info img{
    width: 175px;
    height: 115px;
    margin-right: 35px;
    vertical-align: middle;
}
.alipay{
  display: inline-block;
  height: 48px;
}
.alipay img{
  height: 100%;
  width:auto;
}

.pay-text{
  display: block;
  text-align: right;
  height: 100%;
  line-height: 100%;
  vertical-align: middle;
  margin-top: 20px;
}
.course-price{
    line-height: 28px;
    padding-top: 30px;
}
.course-price .original-price{
    display: block;
    text-decoration: line-through;
    color: #9b9b9b;
}
.course-info img{
    float: left;
}
.course-info .course_name{
    float: left;
    line-height: 28px;
    padding-top: 30px;
}
.course-info .course_name .discount_name{
  display: block;
  height: 14px;
  color: #ffc210;
}
</style>
