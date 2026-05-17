<template>
  <div class="card">
    <h3>登录</h3>
    <div class="form-row"><input v-model="username" placeholder="用户名"/></div>
    <div class="form-row"><input type="password" v-model="password" placeholder="密码"/></div>
    <div style="display:flex;gap:8px;align-items:center">
      <button class="btn" @click="login">登录</button>
      <button class="btn ghost" @click="$router.push('/register')">注册</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data(){return {username:'',password:''}},
  methods:{
    async login(){
      try{
        const r=await axios.post('/api/token/',{username:this.username,password:this.password})
        localStorage.setItem('access',r.data.access)
        localStorage.setItem('refresh',r.data.refresh)
        this.$router.push('/')
      }catch(e){alert('登录失败')}
    }
  }
}
</script>
