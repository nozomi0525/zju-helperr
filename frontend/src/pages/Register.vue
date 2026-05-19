<template>
  <div id="register-page-wrapper" class="register-page">
    <div class="register-card">
      <h3 class="register-title">注册</h3>

      <div class="register-form-row">
        <input v-model="username" placeholder="用户名" />
      </div>

      <div class="register-form-row">
        <input type="password" v-model="password" placeholder="密码" />
      </div>

      <div class="register-actions">
        <button class="register-btn" @click="register">注册</button>
      </div>
    </div>
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

<style>
/* Match the visual style used by Login/Profile but scoped to Register page */
#register-page-wrapper.register-page {
  min-height: 100vh;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  padding: 20px;
  box-sizing: border-box;
}

#register-page-wrapper .register-card {
  background: #ffffff !important;
  border-radius: 16px !important;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1) !important;
  padding: 40px 30px !important;
  width: 100% !important;
  max-width: 400px !important;
  text-align: center !important;
}

#register-page-wrapper .register-title {
  margin: 0 0 30px !important;
  font-size: 28px !important;
  font-weight: 600 !important;
  color: #333 !important;
}

#register-page-wrapper .register-form-row {
  margin-bottom: 20px !important;
}

#register-page-wrapper .register-form-row input {
  width: 100% !important;
  padding: 14px 16px !important;
  font-size: 16px !important;
  border: 1px solid #ddd !important;
  border-radius: 10px !important;
  outline: none !important;
  transition: border-color 0.3s, box-shadow 0.3s !important;
  background: #fafafa !important;
}

#register-page-wrapper .register-form-row input:focus {
  border-color: #667eea !important;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15) !important;
  background: #fff !important;
}

#register-page-wrapper .register-actions {
  display: flex !important;
  gap: 12px !important;
  align-items: center !important;
  margin-top: 10px !important;
}

#register-page-wrapper .register-btn {
  flex: 1 !important;
  padding: 12px 20px !important;
  font-size: 16px !important;
  font-weight: 500 !important;
  border: none !important;
  border-radius: 10px !important;
  cursor: pointer !important;
  background: linear-gradient(135deg, #667eea, #764ba2) !important;
  color: #fff !important;
  transition: transform 0.2s, box-shadow 0.2s, opacity 0.2s !important;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
}

#register-page-wrapper .register-btn:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 18px rgba(102, 126, 234, 0.5) !important;
}

#register-page-wrapper .register-btn:active {
  transform: translateY(0) !important;
}
</style>
