<template>
  <div>
    <div class="card">
      <h3>我的主页</h3>
      <div v-if="!me">请先登录</div>
      <div v-else>
        <div>用户名：{{me.username}}</div>
        <div>信用分：{{me.credit_score}}</div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data(){return {me:null}},
  async mounted(){
    const token=localStorage.getItem('access')
    if(!token) return
    try{const r=await axios.get('/api/users/me/',{headers:{Authorization:'Bearer '+token}});this.me=r.data}catch(e){this.me=null}
  }
}
</script>
