<template>
  <div id="publish-page-wrapper" class="login-page">
    <div class="login-card">
      <h3 class="login-title">发布任务</h3>

      <div class="login-form-row">
        <select v-model="form.category">
          <option value="carpool">拼车</option>
          <option value="errand">跑腿</option>
          <option value="agency">代办</option>
          <option value="emergency">特需</option>
        </select>
      </div>

      <div class="login-form-row">
        <input v-model="form.title" placeholder="标题（简短清晰）" />
      </div>

      <div class="login-form-row">
        <input v-model="form.location" placeholder="位置（单个位置/往返位置）" />
      </div>

      <div class="login-form-row">
        <input v-model="form.deadline" type="text" placeholder="时间" />
      </div>

      <div class="login-form-row" style="display:flex;gap:12px;align-items:center">
        <label style="display:flex;align-items:center;gap:8px;margin:0">
          <input type="radio" value="free" v-model="form.payment" /> 无偿
        </label>
        <label style="display:flex;align-items:center;gap:8px;margin:0">
          <input type="radio" value="paid" v-model="form.payment" /> 有偿
        </label>
        <div style="flex:1;color:#64748b;font-size:12px;text-align:right">有偿时填写报酬描述</div>
      </div>

      <div class="login-form-row" v-if="form.payment==='paid'">
        <input v-model="form.reward" placeholder="报酬描述" />
      </div>

      <div class="login-form-row">
        <input v-model="form.remark" placeholder="任务说明" />
      </div>

      <div class="login-actions">
        <button class="login-btn login-btn-ghost" @click="$router.back()">取消</button>
        <button class="login-btn" @click="publish">发布</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      form: {
        category: 'carpool',
        title: '',
        location: '',
        deadline: '',
        payment: 'free',
        reward: '',
        remark: ''
      }
    }
  },
  methods: {
    async publish() {
      if (!this.form.title.trim()) { alert('请填写标题'); return }
      if (!this.form.location.trim()) { alert('请填写地点'); return }
      if (!this.form.deadline) { alert('请填写时间'); return }
      if (this.form.payment === 'paid' && !this.form.reward.trim()) {
        alert('请选择有偿并填写报酬描述')
        return
      }
      try {
        const token = localStorage.getItem('access')
        if (!token) { alert('请先登录'); return }
        // prepare payload to match backend expectations
        const payload = {
          category: this.form.category,
          title: this.form.title,
          location: this.form.location,
          deadline: this.form.deadline,
          remark: this.form.remark,
          is_paid: this.form.payment === 'paid'
        }
        if (this.form.payment === 'paid') payload.reward = this.form.reward

        await axios.post('/api/tasks/', payload, { headers: { Authorization: 'Bearer ' + token } })
        alert('发布成功')
        this.$router.push('/')
      } catch (e) {
        console.error(e)
        alert('发布失败，请稍后重试')
      }
    }
  }
}
</script>

<style>
/* Match login page style but scoped to publish wrapper */
#publish-page-wrapper.login-page {
  min-height: 100vh;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  padding: 20px;
  box-sizing: border-box;
}

#publish-page-wrapper .login-card {
  background: #ffffff !important;
  border-radius: 16px !important;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08) !important;
  padding: 36px 28px !important;
  width: 100% !important;
  max-width: 520px !important;
  text-align: left !important;
}

#publish-page-wrapper .login-title {
  margin: 0 0 18px !important;
  font-size: 22px !important;
  font-weight: 600 !important;
  color: #0f172a !important;
  text-align: center !important;
}

#publish-page-wrapper .login-form-row { margin-bottom: 14px !important }
#publish-page-wrapper .login-form-row input,
#publish-page-wrapper .login-form-row select {
  width: 100% !important;
  padding: 12px 14px !important;
  font-size: 15px !important;
  border: 1px solid #e6e9ef !important;
  border-radius: 10px !important;
  outline: none !important;
  transition: border-color 0.2s, box-shadow 0.2s !important;
  background: #fff !important;
}

#publish-page-wrapper .login-form-row input:focus,
#publish-page-wrapper .login-form-row select:focus {
  border-color: #667eea !important;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.08) !important;
}

#publish-page-wrapper .login-actions { display:flex !important; gap:12px !important; margin-top:6px !important }
#publish-page-wrapper .login-btn {
  flex: 1 !important;
  padding: 12px 18px !important;
  font-size: 15px !important;
  font-weight: 600 !important;
  border: none !important;
  border-radius: 10px !important;
  cursor: pointer !important;
  background: linear-gradient(135deg, #667eea, #764ba2) !important;
  color: #fff !important;
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.18) !important;
}

#publish-page-wrapper .login-btn-ghost {
  background: transparent !important;
  color: #667eea !important;
  border: 2px solid #667eea !important;
  box-shadow: none !important;
}

#publish-page-wrapper .login-btn-ghost:hover { background:#667eea !important; color:#fff !important }

</style>
