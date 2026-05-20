<template>
  <div class="card task-detail-card">
    <div class="detail-header">
      <div>
        <h3>{{task.title}}</h3>
        <div class="detail-meta">
          <span>分类：{{task.category || '未知'}}</span>
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
        <div class="detail-label">截止时间</div>
        <div class="detail-value">{{deadlineText}}</div>
      </div>
    </div>

    <div class="detail-section">
      <div class="section-title">任务说明</div>
      <p class="section-content">{{task.remark || '暂无补充说明。'}}</p>
    </div>

    <div class="detail-actions">
      <button class="btn" @click="accept" v-if="logged">接单</button>
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
    statusText() {
      if (!this.task.status) return '未知状态'
      if (this.task.status === 'active') return '进行中'
      if (this.task.status === 'completed') return '已完成'
      if (this.task.status === 'expired') return '已过期'
      return this.task.status
    },
    statusClass() {
      if (this.task.status === 'active') return 'status-active'
      if (this.task.status === 'completed') return 'status-completed'
      if (this.task.status === 'expired') return 'status-expired'
      return 'status-default'
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
      if (!this.task.deadline) return '未设置'
      const date = new Date(this.task.deadline)
      return isNaN(date) ? this.task.deadline : date.toLocaleString()
    },
  },
  async mounted() {
    const id = this.$route.params.id
    const r = await axios.get('/api/tasks/' + id + '/')
    this.task = r.data
    this.logged = !!localStorage.getItem('access')
  },
  methods: {
    async accept() {
      try {
        const token = localStorage.getItem('access')
        await axios.post(
          '/api/orders/',
          { task: this.task.id },
          { headers: { Authorization: 'Bearer ' + token } }
        )
        alert('接单成功')
        this.$router.push('/')
      } catch (e) {
        alert('接单失败，请重试')
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
</style>
