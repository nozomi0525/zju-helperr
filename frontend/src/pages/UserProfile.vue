<template>
  <div class="user-profile-page">
    <div class="profile-card">
      <h3 class="profile-title">用户主页</h3>
      <div v-if="loading" class="profile-loading">加载中…</div>
      <div v-else-if="error" class="profile-error">{{ error }}</div>
      <div v-else>
        <div class="profile-summary">
          <div class="profile-name">{{ user.username }}</div>
          <div class="profile-subtitle">信用分 {{ formatScore(user.credit_score) }} <span v-if="user.credit_level">（{{ user.credit_level }}）</span></div>
        </div>
        <div class="profile-stats">
          <div class="profile-stat">
            <div class="profile-stat-num">{{ user.publish_count ?? 0 }}</div>
            <div class="profile-stat-label">发布</div>
          </div>
          <div class="profile-stat">
            <div class="profile-stat-num">{{ user.accept_count ?? 0 }}</div>
            <div class="profile-stat-label">接单</div>
          </div>
          <div class="profile-stat">
            <div class="profile-stat-num">{{ user.review_count ?? 0 }}</div>
            <div class="profile-stat-label">评价</div>
          </div>
        </div>
        <div class="profile-actions">
          <button class="btn" @click="$router.push('/')">返回帖子</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      user: null,
      loading: false,
      error: '',
    }
  },
  async mounted() {
    await this.fetchUser()
  },
  methods: {
    async fetchUser() {
      this.loading = true
      this.error = ''
      const id = this.$route.params.id
      try {
        const r = await axios.get(`/api/users/${id}/`)
        this.user = r.data
      } catch (e) {
        this.error = '用户信息加载失败，请重试'
      } finally {
        this.loading = false
      }
    },
    formatScore(score) {
      const n = Number(score)
      return Number.isFinite(n) ? n.toFixed(1) : '—'
    },
  },
}
</script>

<style scoped>
.user-profile-page {
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}
.profile-card {
  width: 100%;
  max-width: 420px;
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 24px 60px rgba(15, 23, 42, 0.12);
  padding: 28px;
}
.profile-title {
  margin: 0 0 20px;
  font-size: 1.4rem;
  color: #111827;
}
.profile-loading,
.profile-error {
  color: #475569;
  font-size: 0.95rem;
}
.profile-summary {
  margin-bottom: 24px;
}
.profile-name {
  font-size: 1.2rem;
  font-weight: 700;
  color: #0f172a;
}
.profile-subtitle {
  margin-top: 8px;
  color: #475569;
  font-size: 0.95rem;
}
.profile-stats {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}
.profile-stat {
  background: #f8fafc;
  border-radius: 14px;
  padding: 16px;
  text-align: center;
}
.profile-stat-num {
  font-size: 1.2rem;
  font-weight: 700;
  color: #0f172a;
}
.profile-stat-label {
  margin-top: 6px;
  font-size: 0.85rem;
  color: #64748b;
}
.profile-actions {
  display: flex;
  justify-content: center;
}
</style>
