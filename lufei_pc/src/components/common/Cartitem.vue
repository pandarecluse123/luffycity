<template>
    <div class="cart_item">
      <div class="cart_column column_1">
        <el-checkbox class="my_el_checkbox" v-model="cart.select"></el-checkbox>
      </div>
      <div class="cart_column column_2">
        <img :src="cart.image" alt="">
        <span><router-link :to="`/course/${cart.id}`">{{cart.name}}</router-link></span>
      </div>
      <div class="cart_column column_3">
        <el-select v-model="expire" size="mini" placeholder="请选择购买有效期" class="my_el_select">
          <el-option :label="expire.expire_text" :value="expire.expire_time" :key="expire.expire_time" v-for="expire in cart.expire_list"></el-option>
        </el-select>
      </div>
      <div class="cart_column column_4">¥{{cart.price}}</div>
      <div class="cart_column column_4" @click="del">删除</div>
    </div>
</template>

<script>
export default {
    name: "CartItem",
    data(){
      return {
          expire:0,
        checked:false,
      }
    },
    props:['cart'],
    watch:{
      'cart.select':function () {
         this.changeselect()
          this.$emit('changeprice')
        },
        'expire':function (value) {
          this.change_expire(),
            this.cart.expire_list.forEach((item,key)=>{
                if(item.expire_time==value){
                    this.cart.price=item.real_price;
                }

                this.$emit('changeprice')
            })
        }
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

        change_expire(){
            this.$axios.put(`${this.$settings.Host}/cart/course/put/`, {
                course_id: this.cart.id,
                expire: this.expire
            },{
                headers:{
                    'Authorization':'jwt '+this.check_user()
                }
            }
          ).then(response=>{
              this.$message('状态勾选成功')
          }).catch(error=>{
              this.$message('出现问题')
          });
        },

        del(){
          this.$axios.delete(`${this.$settings.Host}/cart/course/delete/`,{
              params:{
                  course_id:this.cart.id
              },
          },{
              headers:{
                  'Authorization':'jwt '+this.check_user()
              }
          }).then(response=>{
              console.log(response.data)
          }).catch(error=>{
              this.$message('出现问题')
          });
            this.$emit('del',this.cart.id)
        },

        changeselect(){
            let course_id=this.cart.id;
            let selected=this.cart.select;
          this.$axios.patch(`${this.$settings.Host}/cart/course/patch/`,{
              course_id,
              selected
          },{
              headers:{
                  'Authorization':'jwt '+this.check_user()
              }
          }).then(response=>{
             this.$message('勾选状态变更成功')
          }).catch(error=>{
              this.$message(error.response.data.message)
          })
        }
    }
}
</script>

<style scoped>
.cart_item::after{
  content: "";
  display: block;
  clear: both;
}
.cart_column{
  float: left;
  height: 250px;
}
.cart_item .column_1{
  width: 88px;
  position: relative;
}
.my_el_checkbox{
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  top: 0;
  margin: auto;
  width: 16px;
  height: 16px;
}
.cart_item .column_2 {
  padding: 67px 10px;
  width: 520px;
  height: 116px;
}
.cart_item .column_2 img{
  width: 175px;
  height: 115px;
  margin-right: 35px;
  vertical-align: middle;
}
.cart_item .column_3{
  width: 197px;
  position: relative;
  padding-left: 10px;
}
.my_el_select{
  width: 117px;
  height: 28px;
  position: absolute;
  top: 0;
  bottom: 0;
  margin: auto;
}
.cart_item .column_4{
  padding: 67px 10px;
  height: 116px;
  width: 142px;
  line-height: 116px;
}

</style>
