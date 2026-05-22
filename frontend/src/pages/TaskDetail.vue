<template>
  <div class="card task-detail-card">
    <div class="detail-header">
      <div>
        <h3>{{task.title}}</h3>
        <div class="detail-meta">
          <span>分类：{{categoryText}}</span>
          <span>位置：{{task.location || '未填写'}}</span>
        </div>
      </div>
      <div :class="['status-chip', statusClass]">{{statusText}}</div>
    </div>

    <div class="detail-grid">
      <div class="detail-block">
        <div class="detail-label">发布者</div>
        <div class="detail-value">{{task.publisher?.username || '匿名'}}</div>
      </div>
      <div class="detail-block">
        <div class="detail-label">奖励</div>
        <div class="detail-value">{{formattedReward}}</div>
      </div>
      <div class="detail-block">
        <div class="detail-label">时间</div>
        <div class="detail-value">{{deadlineText}}</div>
      </div>
    </div>

    <div class="detail-section">
      <div class="section-title">任务说明</div>
      <p class="section-content">{{task.remark || '暂无补充说明。'}}</p>
    </div>

    <div class="detail-section contact-section" v-if="task.publisher_contact">
      <div class="section-title">发布者联系方式</div>
      <p class="section-content contact-value">{{ task.publisher_contact }}</p>
      <p class="contact-tip">此信息仅对接单者可见，请勿随意传播。</p>
    </div>

    <div class="detail-actions">
      <button
        v-if="logged"
        class="btn"
        :class="{ 'btn-disabled': !canAccept }"
        :disabled="!canAccept"
        @click="accept"
      >{{ acceptButtonText }}</button>
      <div class="hint-text" v-else>请登录后接单，或返回帖子列表浏览更多任务。</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      task: {},
      logged: false,
    }
  },
  computed: {
    categoryText() {
      const map = {
        carpool: '拼车',
        errand: '跑腿',
        agency: '代办',
        emergency: '特需',
      }
      if (!this.task || !this.task.category) return '未知'
      return map[this.task.category] || this.task.category
    },
    statusText() {
      if (!this.task.status) return '未知状态'
      if (this.task.status === 'active') return '进行中'
      if (this.task.status === 'accepted') return '已接单'
      if (this.task.status === 'completed') return '已完成'
      if (this.task.status === 'expired') return '已过期'
      return this.task.status
    },
    statusClass() {
      if (this.task.status === 'active') return 'status-active'
      if (this.task.status === 'accepted') return 'status-accepted'
      if (this.task.status === 'completed') return 'status-completed'
      if (this.task.status === 'expired') return 'status-expired'
      return 'status-default'
    },
    canAccept() {
      return this.task.status === 'active' && this.logged
    },
    acceptButtonText() {
      if (this.task.status === 'accepted') return '已接单'
      if (this.task.status === 'completed') return '已完成'
      if (this.task.status === 'expired') return '已过期'
      return '接单'
    },
    formattedReward() {
      if (!this.task) return ''
      if (!this.task.is_paid) return '无偿'
      if (!this.task.reward) return '面议'
      // If reward looks like a number, show currency symbol; otherwise display as-is
      const r = String(this.task.reward).trim()
      return /^\d+(\.\d+)?$/.test(r) ? `¥${r}` : r
    },
    deadlineText() {
      return this.task.deadline || '未设置'
    },
  },
  async mounted() {
    await this.loadTask()
    this.logged = !!localStorage.getItem('access')
  },
  methods: {
    async loadTask() {
      const id = this.$route.params.id
      const r = await axios.get('/api/tasks/' + id + '/')
      this.task = r.data
    },
    async accept() {
      if (!this.canAccept) return
      try {
        await axios.post('/api/orders/', { task: this.task.id })
        alert('接单成功')
        await this.loadTask()
      } catch (e) {
        const msg = e.response?.data?.detail
          || (e.response?.data && Object.values(e.response.data).flat().join(' '))
          || '接单失败，请重试'
        alert(msg)
        await this.loadTask()
      }
    },
  },
}
</script>

<style>
.task-detail-card {
  max-width: 780px;
  margin: 0 auto;
}
.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 20px;
}
.detail-header h3 {
  margin: 0 0 10px;
  font-size: 1.6rem;
}
.detail-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 24px;
  color: #475569;
  font-size: 0.95rem;
}
.status-chip {
  display: inline-flex;
  align-items: center;
  padding: 8px 12px;
  border-radius: 999px;
  font-size: 0.9rem;
  font-weight: 600;
}
.status-active {
  background: #e0f2fe;
  color: #0369a1;
}
.status-completed {
  background: #dcfce7;
  color: #166534;
}
.status-expired {
  background: #fee2e2;
  color: #991b1b;
}
.status-accepted {
  background: #fee2e2;
  color: #dc2626;
}
.status-default {
  background: #e2e8f0;
  color: #334155;
}
.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 14px;
}
.detail-block {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 16px;
}
.detail-label {
  color: #64748b;
  font-size: 0.85rem;
  margin-bottom: 8px;
}
.detail-value {
  font-size: 1rem;
  color: #0f172a;
  font-weight: 600;
}
.detail-section {
  margin-top: 22px;
}
.section-title {
  margin-bottom: 10px;
  font-size: 1rem;
  font-weight: 700;
  color: #0f172a;
}
.section-content {
  margin: 0;
  color: #334155;
  line-height: 1.8;
}
.contact-section {
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 12px;
  padding: 16px 18px;
}
.contact-value {
  font-weight: 600;
  color: #b91c1c;
  font-size: 1.05rem;
}
.contact-tip {
  margin: 10px 0 0;
  font-size: 0.85rem;
  color: #991b1b;
}
.detail-actions {
  margin-top: 24px;
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
}
.hint-text {
  color: #64748b;
  font-size: 0.95rem;
}
.btn-disabled,
.btn:disabled {
  background: #cbd5e1 !important;
  color: #64748b !important;
  cursor: not-allowed;
  box-shadow: none;
}
</style>
