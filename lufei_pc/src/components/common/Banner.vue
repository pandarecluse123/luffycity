<template>
  <div class="banner">
      <el-carousel trigger="click" height="506px">
      <el-carousel-item v-for="item,key in banner_list" :key="key">
        <a :href="item.link"><img :src="item.image"></a>
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<script>
  export default {
    name:"Banner",
    data(){
      return {
        banner_list:[],
      };
    },
    created: function(){
      // 获取轮播图
      this.$axios.get(`${this.$settings.Host}/banner/`).then(response => {
        this.banner_list = response.data
      }).catch(error => {
        console.log(error.response);
      });
    }
  }
</script>
