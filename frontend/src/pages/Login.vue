<template>
  <div id="login-page-wrapper" class="login-page">
    <div class="login-card">
      <h3 class="login-title">登录</h3>
      <div class="login-form-row">
        <input v-model="username" placeholder="用户名" />
      </div>
      <div class="login-form-row">
        <input type="password" v-model="password" placeholder="密码" />
      </div>
      <div class="login-actions">
        <button type="button" class="login-btn" @click="login">登录</button>
      </div>
      <p class="login-footer">
        没有账号？
        <router-link to="/register" class="login-register-link">注册</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return { username: '', password: '' }
  },
  methods: {
    async login() {
      try {
        const r = await axios.post('/api/token/', {
          username: this.username,
          password: this.password
        })
        localStorage.setItem('access', r.data.access)
        localStorage.setItem('refresh', r.data.refresh)
        this.$router.push('/')
      } catch (e) {
        alert('登录失败')
      }
    }
  }
}
</script>

<style>
/* 使用 ID + 类 组合选择器，确保最高优先级 */
#login-page-wrapper.login-page {
  min-height: 100vh;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  padding: 20px;
  box-sizing: border-box;
}

#login-page-wrapper .login-card {
  background: #ffffff !important;
  border-radius: 16px !important;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1) !important;
  padding: 40px 30px !important;
  width: 100% !important;
  max-width: 400px !important;
  text-align: center !important;
}

#login-page-wrapper .login-title {
  margin: 0 0 30px !important;
  font-size: 28px !important;
  font-weight: 600 !important;
  color: #333 !important;
}

#login-page-wrapper .login-form-row {
  margin-bottom: 20px !important;
}

#login-page-wrapper .login-form-row input {
  width: 100% !important;
  padding: 14px 16px !important;
  font-size: 16px !important;
  border: 1px solid #ddd !important;
  border-radius: 10px !important;
  outline: none !important;
  transition: border-color 0.3s, box-shadow 0.3s !important;
  background: #fafafa !important;
}

#login-page-wrapper .login-form-row input:focus {
  border-color: #667eea !important;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15) !important;
  background: #fff !important;
}

#login-page-wrapper .login-actions {
  margin-top: 10px !important;
}

#login-page-wrapper .login-btn {
  display: block !important;
  width: 100% !important;
  padding: 14px 20px !important;
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

#login-page-wrapper .login-btn:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 18px rgba(102, 126, 234, 0.5) !important;
}

#login-page-wrapper .login-btn:active {
  transform: translateY(0) !important;
}

#login-page-wrapper .login-footer {
  margin: 24px 0 0 !important;
  font-size: 14px !important;
  color: #888 !important;
}

#login-page-wrapper .login-register-link {
  color: #667eea !important;
  font-weight: 500 !important;
  text-decoration: none !important;
  transition: color 0.2s !important;
}

#login-page-wrapper .login-register-link:hover {
  color: #764ba2 !important;
  text-decoration: underline !important;
}
</style>
