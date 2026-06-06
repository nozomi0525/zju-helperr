<template>
  <div id="publish-page-wrapper" class="login-page">
    <div class="login-card" :class="{ 'login-card-dimmed': showGuideModal }">
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
        <input v-model="form.deadline" type="text" placeholder="日期+具体时间段" />
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

      <div class="login-form-row">
        <input v-model="form.contact_info" placeholder="联系方式（仅接单人可见，如手机号/微信）" />
      </div>
      <p class="contact-hint">为保护隐私，联系方式不会在列表中展示，仅成功接单的用户可在详情页查看。</p>

      <div class="login-actions">
        <button class="login-btn login-btn-ghost" @click="$router.back()">取消</button>
        <button class="login-btn" :disabled="showGuideModal" @click="publish">发布</button>
      </div>
    </div>

    <div v-if="showGuideModal" class="publish-guide-backdrop">
      <div class="publish-guide-modal" role="dialog" aria-modal="true" aria-labelledby="publish-guide-title">
        <h4 id="publish-guide-title" class="publish-guide-title">分区指南</h4>
        <div class="publish-guide-body">
          <p>欢迎使用 ZJU Helper 校园互助平台！本平台设有四大分区，可精准对接用户需求：</p>
          <p><strong>「拼车」</strong>板块面向日常通勤和出行拼车需求；</p>
          <p><strong>「跑腿」</strong>板块面向外卖快递代取等日常琐事求助；</p>
          <p><strong>「代办」</strong>面向成绩单打印、事务代办、手续办理、资料代交等需要他人代为处理的正式事项；</p>
          <p><strong>「特需」</strong>专为紧急求助（如借伞，卫生巾，充电宝）或临时帮忙等突发情况开设。</p>
          <p>请用户在仔细阅读分区指南后，根据自身需求类型选择对应分区，写明核心诉求等关键信息，以便更快获得响应~</p>
        </div>
        <button type="button" class="login-btn publish-guide-close" @click="closeGuide">我已阅读，开始发帖</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

const GUIDE_SEEN_KEY = 'publish_guide_seen'

export default {
  data() {
    return {
      showGuideModal: sessionStorage.getItem(GUIDE_SEEN_KEY) !== '1',
      form: {
        category: 'carpool',
        title: '',
        location: '',
        deadline: '',
        payment: 'free',
        reward: '',
        remark: '',
        contact_info: ''
      }
    }
  },
  methods: {
    closeGuide() {
      sessionStorage.setItem(GUIDE_SEEN_KEY, '1')
      this.showGuideModal = false
    },
    async publish() {
      if (this.showGuideModal) {
        alert('请先阅读分区指南')
        return
      }
      if (!this.form.title.trim()) { alert('请填写标题'); return }
      if (!this.form.location.trim()) { alert('请填写地点'); return }
      if (!this.form.deadline) { alert('请填写时间'); return }
      if (this.form.payment === 'paid' && !this.form.reward.trim()) {
        alert('请选择有偿并填写报酬描述')
        return
      }
      if (!this.form.contact_info.trim()) {
        alert('请填写联系方式（仅接单人可见）')
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
          contact_info: this.form.contact_info.trim(),
          is_paid: this.form.payment === 'paid'
        }
        if (this.form.payment === 'paid') payload.reward = this.form.reward

        await axios.post('/api/tasks/', payload)
        alert('发布成功')
        this.$router.push('/')
      } catch (e) {
        console.error(e)
        const data = e.response?.data
        let msg = '发布失败，请稍后重试'
        if (data) {
          if (typeof data.detail === 'string') msg = data.detail
          else if (typeof data === 'object') {
            msg = Object.entries(data)
              .map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(' ') : v}`)
              .join('\n')
          }
        }
        alert(msg)
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

#publish-page-wrapper .contact-hint {
  margin: -6px 0 14px !important;
  font-size: 12px !important;
  color: #64748b !important;
  line-height: 1.5 !important;
}

#publish-page-wrapper .login-card-dimmed {
  pointer-events: none !important;
  user-select: none !important;
  filter: blur(1px) !important;
  opacity: 0.72 !important;
}

#publish-page-wrapper .publish-guide-backdrop {
  position: fixed !important;
  inset: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 20px !important;
  background: rgba(15, 23, 42, 0.45) !important;
  z-index: 1000 !important;
}

#publish-page-wrapper .publish-guide-modal {
  width: 100% !important;
  max-width: 520px !important;
  max-height: 85vh !important;
  overflow-y: auto !important;
  background: #ffffff !important;
  border-radius: 16px !important;
  box-shadow: 0 24px 48px rgba(15, 23, 42, 0.18) !important;
  padding: 28px 24px 24px !important;
}

#publish-page-wrapper .publish-guide-title {
  margin: 0 0 16px !important;
  font-size: 20px !important;
  font-weight: 700 !important;
  color: #0f172a !important;
  text-align: center !important;
}

#publish-page-wrapper .publish-guide-body {
  font-size: 14px !important;
  line-height: 1.75 !important;
  color: #334155 !important;
}

#publish-page-wrapper .publish-guide-body p {
  margin: 0 0 12px !important;
}

#publish-page-wrapper .publish-guide-body p:last-child {
  margin-bottom: 0 !important;
}

#publish-page-wrapper .publish-guide-close {
  width: 100% !important;
  margin-top: 20px !important;
}

#publish-page-wrapper .login-btn:disabled {
  opacity: 0.5 !important;
  cursor: not-allowed !important;
  transform: none !important;
  box-shadow: none !important;
}

</style>
