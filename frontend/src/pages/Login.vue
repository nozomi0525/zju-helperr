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
        <button class="login-btn" @click="login">登录</button>
        <button class="login-btn login-btn-ghost" @click="$router.push('/register')">注册</button>
      </div>
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
  display: flex !important;
  gap: 12px !important;
  align-items: center !important;
  margin-top: 10px !important;
}

#login-page-wrapper .login-btn {
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

#login-page-wrapper .login-btn:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 18px rgba(102, 126, 234, 0.5) !important;
}

#login-page-wrapper .login-btn:active {
  transform: translateY(0) !important;
}

#login-page-wrapper .login-btn-ghost {
  background: transparent !important;
  color: #667eea !important;
  border: 2px solid #667eea !important;
  box-shadow: none !important;
}

#login-page-wrapper .login-btn-ghost:hover {
  background: #667eea !important;
  color: #fff !important;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
}
</style>
