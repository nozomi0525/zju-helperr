<template>
  <div class="card">
    <h3>注册</h3>
    <div class="form-row"><input v-model="username" placeholder="用户名"/></div>
    <div class="form-row"><input type="password" v-model="password" placeholder="密码"/></div>
    <div><button class="btn" @click="register">注册</button></div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data(){return {username:'',password:''}},
  methods:{
    async register(){
      try{
        console.log('Register attempt', {username: this.username})
        const r = await axios.post('/api/users/',{username:this.username,password:this.password})
        console.log('Register response', r.status, r.data)
        alert('注册成功，请登录')
        this.$router.push('/login')
      }catch(e){
        console.error('Register error', e)
        let msg = '注册失败'
        if(e.response && e.response.data){
          const data = e.response.data
          if(typeof data === 'string') msg = data
          else if(data.detail) msg = data.detail
          else {
            msg = Object.entries(data).map(([k,v]) => `${k}: ${Array.isArray(v)?v.join(' '):v}`).join('\n')
          }
        }
        alert(msg)
      }
    }
  }
}
</script>
