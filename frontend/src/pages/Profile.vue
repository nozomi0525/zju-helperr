<template>
  <div id="profile-page-wrapper" class="profile-page">
    <div class="profile-card">
      <h3 class="profile-title">我的主页</h3>

      <div v-if="loading" class="profile-loading">
        <p class="profile-loading-text">加载中…</p>
      </div>

      <div v-else-if="loadError" class="profile-empty">
        <p class="profile-empty-text">{{ loadError }}</p>
        <div class="profile-actions">
          <button class="profile-btn" @click="fetchMe">重试</button>
          <button class="profile-btn profile-btn-ghost" @click="goLogin">重新登录</button>
        </div>
      </div>

      <div v-else-if="!isLoggedIn" class="profile-empty">
        <div class="profile-empty-icon">👤</div>
        <p class="profile-empty-text">请先登录后查看个人信息</p>
        <div class="profile-actions">
          <button class="profile-btn" @click="$router.push('/login')">去登录</button>
          <button class="profile-btn profile-btn-ghost" @click="$router.push('/register')">注册账号</button>
        </div>
      </div>

      <div v-else class="profile-content">
        <div class="profile-header">
          <div class="profile-avatar">
            <img v-if="me.avatar" :src="me.avatar" alt="头像" />
            <span v-else class="profile-avatar-letter">{{ avatarLetter }}</span>
          </div>
          <div class="profile-identity">
            <div class="profile-username">{{ me.username }}</div>
            <div v-if="displayName" class="profile-nickname">{{ displayName }}</div>
          </div>
        </div>

        <div class="profile-credit">
          <span class="profile-credit-label">信用分</span>
          <span class="profile-credit-value">{{ formatScore(me.credit_score) }}</span>
          <div class="profile-credit-bar">
            <div class="profile-credit-fill" :style="{ width: creditPercent + '%' }"></div>
          </div>
        </div>

        <div class="profile-stats">
          <div class="profile-stat">
            <span class="profile-stat-num">{{ me.publish_count ?? 0 }}</span>
            <span class="profile-stat-label">发布</span>
          </div>
          <div class="profile-stat-divider"></div>
          <div class="profile-stat">
            <span class="profile-stat-num">{{ me.accept_count ?? 0 }}</span>
            <span class="profile-stat-label">接单</span>
          </div>
        </div>

        <div v-if="hasContact" class="profile-info">
          <div v-if="me.phone" class="profile-info-row">
            <span class="profile-info-key">手机</span>
            <span class="profile-info-val">{{ me.phone }}</span>
          </div>
          <div v-if="me.wechat" class="profile-info-row">
            <span class="profile-info-key">微信</span>
            <span class="profile-info-val">{{ me.wechat }}</span>
          </div>
        </div>

        <div class="profile-actions profile-actions-single">
          <button class="profile-btn" @click="$router.push('/')">浏览帖子</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return { me: null, loading: false, loadError: '' }
  },
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem('access')
    },
    avatarLetter() {
      const name = this.me?.username || '?'
      return name.charAt(0).toUpperCase()
    },
    displayName() {
      if (!this.me) return ''
      const parts = [this.me.first_name, this.me.last_name].filter(Boolean)
      return parts.join(' ').trim()
    },
    hasContact() {
      return this.me && (this.me.phone || this.me.wechat)
    },
    creditPercent() {
      const score = Number(this.me?.credit_score ?? 5)
      return Math.min(100, Math.max(0, (score / 5) * 100))
    }
  },
  mounted() {
    this.fetchMe()
  },
  methods: {
    async fetchMe() {
      if (!this.isLoggedIn) {
        this.me = null
        this.loadError = ''
        this.loading = false
        return
      }
      this.loading = true
      this.loadError = ''
      try {
        const r = await axios.get('/api/users/me/')
        this.me = r.data
      } catch (e) {
        this.me = null
        const status = e.response?.status
        if (status === 401) {
          localStorage.removeItem('access')
          localStorage.removeItem('refresh')
          this.loadError = '登录已过期，请重新登录'
        } else {
          this.loadError = '加载个人信息失败，请检查网络后重试'
        }
      } finally {
        this.loading = false
      }
    },
    goLogin() {
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
      this.$router.push('/login')
    },
    formatScore(score) {
      const n = Number(score)
      return Number.isFinite(n) ? n.toFixed(1) : '—'
    }
  }
}
</script>

<style>
#profile-page-wrapper.profile-page {
  min-height: calc(100vh - 120px);
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  padding: 20px;
  box-sizing: border-box;
  margin: -12px -12px 0;
  border-radius: 12px;
}

#profile-page-wrapper .profile-card {
  background: #ffffff !important;
  border-radius: 16px !important;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1) !important;
  padding: 40px 30px !important;
  width: 100% !important;
  max-width: 400px !important;
  text-align: center !important;
}

#profile-page-wrapper .profile-title {
  margin: 0 0 28px !important;
  font-size: 28px !important;
  font-weight: 600 !important;
  color: #333 !important;
}

#profile-page-wrapper .profile-loading {
  padding: 24px 0;
}

#profile-page-wrapper .profile-loading-text {
  margin: 0;
  color: #64748b;
  font-size: 15px;
}

#profile-page-wrapper .profile-empty {
  padding: 8px 0 4px;
}

#profile-page-wrapper .profile-empty-icon {
  font-size: 48px;
  line-height: 1;
  margin-bottom: 12px;
  opacity: 0.85;
}

#profile-page-wrapper .profile-empty-text {
  margin: 0 0 24px;
  color: #64748b;
  font-size: 15px;
}

#profile-page-wrapper .profile-header {
  display: flex;
  align-items: center;
  gap: 16px;
  text-align: left;
  margin-bottom: 24px;
}

#profile-page-wrapper .profile-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  background: linear-gradient(135deg, #667eea, #764ba2);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.35);
}

#profile-page-wrapper .profile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

#profile-page-wrapper .profile-avatar-letter {
  font-size: 26px;
  font-weight: 600;
  color: #fff;
}

#profile-page-wrapper .profile-identity {
  min-width: 0;
}

#profile-page-wrapper .profile-username {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  word-break: break-all;
}

#profile-page-wrapper .profile-nickname {
  margin-top: 4px;
  font-size: 14px;
  color: #64748b;
}

#profile-page-wrapper .profile-credit {
  background: #fafafa;
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 20px;
  text-align: left;
}

#profile-page-wrapper .profile-credit-label {
  font-size: 13px;
  color: #64748b;
  margin-right: 8px;
}

#profile-page-wrapper .profile-credit-value {
  font-size: 22px;
  font-weight: 700;
  color: #667eea;
}

#profile-page-wrapper .profile-credit-bar {
  margin-top: 10px;
  height: 6px;
  background: #e8ecf4;
  border-radius: 3px;
  overflow: hidden;
}

#profile-page-wrapper .profile-credit-fill {
  height: 100%;
  border-radius: 3px;
  background: linear-gradient(90deg, #667eea, #764ba2);
  transition: width 0.4s ease;
}

#profile-page-wrapper .profile-stats {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0;
  margin-bottom: 20px;
  padding: 16px 0;
  border-top: 1px solid #f0f0f0;
  border-bottom: 1px solid #f0f0f0;
}

#profile-page-wrapper .profile-stat {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

#profile-page-wrapper .profile-stat-num {
  font-size: 24px;
  font-weight: 700;
  color: #333;
}

#profile-page-wrapper .profile-stat-label {
  font-size: 13px;
  color: #94a3b8;
}

#profile-page-wrapper .profile-stat-divider {
  width: 1px;
  height: 36px;
  background: #e8ecf4;
}

#profile-page-wrapper .profile-info {
  text-align: left;
  margin-bottom: 20px;
}

#profile-page-wrapper .profile-info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #fafafa;
  border: 1px solid #eee;
  border-radius: 10px;
  margin-bottom: 10px;
  font-size: 15px;
}

#profile-page-wrapper .profile-info-row:last-child {
  margin-bottom: 0;
}

#profile-page-wrapper .profile-info-key {
  color: #64748b;
}

#profile-page-wrapper .profile-info-val {
  color: #333;
  font-weight: 500;
}

#profile-page-wrapper .profile-actions {
  display: flex !important;
  gap: 12px !important;
  align-items: center !important;
  margin-top: 4px !important;
}

#profile-page-wrapper .profile-actions-single {
  margin-top: 8px !important;
}

#profile-page-wrapper .profile-btn {
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

#profile-page-wrapper .profile-btn:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 18px rgba(102, 126, 234, 0.5) !important;
}

#profile-page-wrapper .profile-btn:active {
  transform: translateY(0) !important;
}

#profile-page-wrapper .profile-btn-ghost {
  background: transparent !important;
  color: #667eea !important;
  border: 2px solid #667eea !important;
  box-shadow: none !important;
}

#profile-page-wrapper .profile-btn-ghost:hover {
  background: #667eea !important;
  color: #fff !important;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
}
</style>
