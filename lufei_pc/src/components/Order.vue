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

      <div class="discount">
        <div id="accordion">
          <div class="coupon-box">
            <div class="icon-box">
              <span class="select-coupon">使用优惠劵：</span>
              <a class="select-icon unselect">
                <img class="sign is_show_select" :class="use_coupon?'is_selected':''" src="../../static/image/12.png"
                     alt="" @click="use_coupon=!use_coupon">
              </a>
              <span class="coupon-num">有{{coupon_list.length}}张可用</span>
            </div>
            <p class="sum-price-wrap">商品总金额：<span class="sum-price">{{this.total}}元</span></p>
          </div>
          <div id="collapseOne" v-if="use_coupon">
            <ul class="coupon-list">
              <li class="coupon-item" v-for="item,key in coupon_list" :key="key" @click="coupon=item.id" :class="check_coupon(item)">
                <p class="coupon-name">{{item.coupon.name}}</p>
                <p class="coupon-condition">满{{item.coupon.condition}}元可以使用</p>
                <p class="coupon-time start_time">开始时间：{{stime(item.start_time)}}</p>
                <p class="coupon-time end_time">过期时间：{{endtime(item.start_time,item.coupon.timer)}}</p>
              </li>
            </ul>
            <div class="no-coupon" v-if="!coupon_list.length">
              <span class="no-coupon-tips">暂无可用优惠券</span>
            </div>
          </div>
        </div>
        <div class="credit-box">
          <label class="my_el_check_box">
            <el-checkbox class="my_el_checkbox" v-model="use_credit"></el-checkbox>
          </label>
          <p class="discount-num1" >使用我的贝里</p>
          <p class="discount-num2" v-if="use_credit"><span>总积分：{{user_credit}}，使用积分
  <el-input-number v-model="credit" :min="1" :max="parseFloat(max_credit())" label="描述文字"></el-input-number>
            剩余积分{{user_credit-credit}}</span></p>
        </div>
        <p class="sun-coupon-num" v-if="use_credit">积分抵扣：<span>{{(credit/credit_to_money).toFixed(2)}}元</span></p>
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
          <el-col :span="8" class="count">实付款： <span>¥{{(this.real_total-credit/credit_to_money).toFixed(2)}}</span></el-col>
          <el-col :span="4" class="cart-pay"><span @click="payHander">去支付</span></el-col>
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
        data() {
            return {
                credit_to_money:localStorage.getItem('credit_to_money') || sessionStorage.getItem('credit_to_money'),
                course_list: [],
                pay_type: 1,
                real_total:0,
                total: 0,
                coupon: 0,
                credit: 0,
                coupon_list: [],
                use_coupon: false,
                use_credit:false,
                user_credit:0,
            }
        },
        watch:{
            'use_coupon':function () {
                    this.coupon=0
            },
            'coupon':function () {
                this.get_real_total()
            }

        },
        components: {
            Header,
            Footer
        },
        created() {
            this.get_total();
            this.get_real_total();
            this.get_course_list();
            this.get_coupon_list();
            this.user_credit=localStorage.getItem('user_credit') || sessionStorage.getItem('user_credit')
        },
        methods: {
            check_user() {
                let user_token = localStorage.getItem('user_token') || sessionStorage.getItem('user_token');
                if (!user_token) {
                    this.$confirm('对不起,请登录后继续操作', '警告').then(() => {
                        this.$router.push('/user/login/');
                    });
                    return false
                }
                return user_token
            },
            check_coupon(coupon){
                let now=(new Date()-0);
                let start=new Date(coupon.start_time )-0;
                let end   = start + coupon.coupon.timer * 24 * 60 * 60 * 1000;
                let disable=false

                if(now<start || now>end){
                    disable=true
                    return 'disable'
                };
                if (!disable && coupon.id==this.coupon){
                    return 'active'
                };
                return ''
            },
            get_course_list() {
                this.$axios.get(`${this.$settings.Host}/cart/course/selected_order/`, {
                        headers: {
                            'Authorization': 'jwt ' + this.check_user()
                        }
                    }
                ).then(response => {
                    this.course_list = response.data;
                    this.get_total();
                     this.get_real_total();
                }).catch(error => {
                    console.log(error.response.data.message)
                });
            },
            get_coupon_list() {
                this.$axios.get(`${this.$settings.Host}/coupon/list/`, {
                        headers: {
                            'Authorization': 'jwt ' + this.check_user()
                        }
                    }
                ).then(response => {
                    this.coupon_list = response.data;

                }).catch(error => {
                    console.log(error.response.data.message)
                });

            },
            payHander() {
                this.$axios.post(`${this.$settings.Host}/order/`, {
                    'pay_type': this.pay_type,
                    'coupon': this.coupon,
                    'credit': this.credit
                }, {
                    headers: {
                        'Authorization': 'jwt ' + this.check_user()
                    }
                }).then(response => {
                    this.get_alipay_url(response.data.order_number)
                }).catch(error => {
                    console.log(error.response)
                })

            },
            get_alipay_url(order_number){
                console.log(order_number)
                this.$axios.post(`${this.$settings.Host}/payments/${order_number}/alipay/`,{
                    headers: {
                        'Authorization': 'jwt ' + this.check_user()
                    }
                }).then(response=>{
                    location.href=response.data.pay_url
                })
            },
            stime(start_time) {
                let stime = start_time.replace('T', ' ');
                stime = stime.slice(0, 19);
                return stime
            },
            endtime(start_time, timer) {

                let time = parseInt(timer) * 60 * 60 * 24 * 1000
                let end_time = new Date(new Date(start_time) - 0 + time)
                let Y = end_time.getFullYear()
                let m = (end_time.getMonth()+1)
                let d = end_time.getDate()
                let H = end_time.getHours()
                let M = end_time.getMinutes()
                let s = end_time.getSeconds()
                m = m > 9 ? m : '0' + m;
                d = d > 9 ? d : '0' + d;
                H = H > 9 ? H : '0' + H;
                M = M > 9 ? M : '0' + M;
                s = s > 9 ? s : '0' + s;
                return Y + "-" + m + "-" + d + " " + H + ":" + M + ":" + s;
            },
            max_credit(){

                if(this.credit>(this.total*this.credit_to_money)){
                    return (this.total*this.credit_to_money)
                }else{
                     return this.user_credit
                }
            },
            get_total() {
                let total = 0
                for (let item in this.course_list) {
                    total += parseFloat(this.course_list[item].real_price)

                }
                this.total = total.toFixed(2)
            },
            get_real_total(){
                 let total = 0
                for (let item in this.course_list) {
                    total += parseFloat(this.course_list[item].real_price)

                }
                total= total.toFixed(2)
                if(this.use_coupon && this.coupon>0){
                for(let item in this.coupon_list){
                    let coupon=this.coupon_list[item]
                    let now=(new Date()-0);
                    let start=new Date(coupon.start_time )-0;
                    let end   = start + coupon.coupon.timer * 24 * 60 * 60 * 1000;
                    if(coupon.id==this.coupon && start<=now && now<=end){
                        if(total>coupon.coupon.condition){
                        let sale_num=parseFloat(coupon.coupon.sale.slice(1))
                        if(coupon.coupon.sale[0]=='-'){
                            total-=sale_num
                        }else if(coupon.coupon.sale[0]=='*'){
                            total*=sale_num
                        }
                    }}
                }
                }
            this.real_total=total
            }
        }
    }


</script>

<style scoped>
  .cart {
    margin-top: 80px;
  }

  .cart-info {
    overflow: hidden;
    width: 1200px;
    margin: auto;
  }

  .cart-top {
    font-size: 18px;
    color: #666;
    margin: 25px 0;
    font-weight: normal;
  }

  .cart-top span {
    font-size: 12px;
    color: #d0d0d0;
    display: inline-block;
  }

  .cart-title {
    background: #F7F7F7;
    height: 70px;
  }

  .calc {
    margin-top: 25px;
    margin-bottom: 40px;
  }

  .calc .count {
    text-align: right;
    margin-right: 10px;
    vertical-align: middle;
  }

  .calc .count span {
    font-size: 36px;
    color: #333;
  }

  .calc .cart-pay {
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

  .cart-item {
    height: 120px;
    line-height: 120px;
    margin-bottom: 30px;
  }

  .course-info img {
    width: 175px;
    height: 115px;
    margin-right: 35px;
    vertical-align: middle;
  }

  .alipay {
    display: inline-block;
    height: 48px;
  }

  .alipay img {
    height: 100%;
    width: auto;
  }

  .pay-text {
    display: block;
    text-align: right;
    height: 100%;
    line-height: 100%;
    vertical-align: middle;
    margin-top: 20px;
  }

  .course-price {
    line-height: 28px;
    padding-top: 30px;
  }

  .course-price .original-price {
    display: block;
    text-decoration: line-through;
    color: #9b9b9b;
  }

  .course-info img {
    float: left;
  }

  .course-info .course_name {
    float: left;
    line-height: 28px;
    padding-top: 30px;
  }

  .course-info .course_name .discount_name {
    display: block;
    height: 14px;
    color: #ffc210;
  }

  .coupon-box {
    text-align: left;
    padding-bottom: 22px;
    padding-left: 30px;
    border-bottom: 1px solid #e8e8e8;
  }

  .coupon-box::after {
    content: "";
    display: block;
    clear: both;
  }

  .icon-box {
    float: left;
  }

  .icon-box .select-coupon {
    float: left;
    color: #666;
    font-size: 16px;
  }

  .icon-box::after {
    content: "";
    clear: both;
    display: block;
  }

  .select-icon {
    width: 20px;
    height: 20px;
    float: left;
  }

  .select-icon img {
    max-height: 100%;
    max-width: 100%;
    margin-top: 2px;
    transform: rotate(-90deg);
    transition: transform .5s;
  }

  .is_show_select {
    transform: rotate(0deg) !important;
  }

  .coupon-num {
    height: 22px;
    line-height: 22px;
    padding: 0 5px;
    text-align: center;
    font-size: 12px;
    float: left;
    color: #fff;
    letter-spacing: .27px;
    background: #fa6240;
    border-radius: 2px;
    margin-left: 20px;
  }

  .sum-price-wrap {
    float: right;
    font-size: 16px;
    color: #4a4a4a;
    margin-right: 45px;
  }

  .sum-price-wrap .sum-price {
    font-size: 18px;
    color: #fa6240;
  }

  .no-coupon {
    text-align: center;
    width: 100%;
    padding: 50px 0px;
    align-items: center;
    justify-content: center; /* 文本两端对其 */
    border-bottom: 1px solid rgb(232, 232, 232);
  }

  .no-coupon-tips {
    font-size: 16px;
    color: #9b9b9b;
  }

  .credit-box {
    height: 30px;
    margin-top: 40px;
    display: flex;
    align-items: center;
    justify-content: flex-end
  }

  .my_el_check_box {
    position: relative;
  }

  .my_el_checkbox {
    margin-right: 10px;
    width: 16px;
    height: 16px;
  }

  .discount-num1 {
    color: #9b9b9b;
    font-size: 16px;
    margin-right: 45px;
  }

  .discount-num2 {
    margin-right: 45px;
    font-size: 16px;
    color: #4a4a4a;
  }

  .sun-coupon-num {
    margin-right: 45px;
    margin-bottom: 43px;
    margin-top: 40px;
    font-size: 16px;
    color: #4a4a4a;
    display: inline-block;
    text-align: right;
    width: 100%;
  }

  .sun-coupon-num span {
    font-size: 18px;
    color: #fa6240;
    margin-right: 40px;
  }

  .coupon-list {
    margin: 20px 0;
  }

  .coupon-list::after {
    display: block;
    content: "";
    clear: both;
  }

  .coupon-item {
    float: left;
    margin: 15px 8px;
    width: 180px;
    height: 100px;
    padding: 5px;
    background-color: #fa3030;
    cursor: pointer;
  }

  .coupon-list .active {
    background-color: #fa9000;
  }

  .coupon-list .disable {
    cursor: not-allowed;
    background-color: #fa6060;
  }

  .coupon-condition {
    font-size: 12px;
    text-align: center;
    color: #fff;
  }

  .coupon-name {
    color: #fff;
    font-size: 24px;
    text-align: center;
  }

  .coupon-time {
    text-align: left;
    color: #fff;
    font-size: 12px;
  }

  .unselect {
    margin-left: 0px;
    transform: rotate(-90deg);
  }

  .is_selected {
    transform: rotate(0.25turn) !important;
  }

.el-icon-minus,.el-icon-plus{
 font-size: 12px;
}
</style>
