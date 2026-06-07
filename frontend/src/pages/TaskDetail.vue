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
        <div class="detail-value">
          <router-link
            v-if="task.publisher?.id"
            :to="`/user/${task.publisher.id}`"
            class="publisher-link"
          >
            {{ task.publisher.username || '匿名' }}
          </router-link>
          <span v-else>{{ task.publisher?.username || '匿名' }}</span>
        </div>
      </div>
      <div class="detail-block">
        <div class="detail-label">信用分</div>
        <div class="detail-value">{{ publisherCreditText }}</div>
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

    <div v-if="orderInfo" class="detail-section order-section">
      <div class="section-title">订单进度</div>
      <p class="order-meta">
        接单人：{{ orderInfo.acceptor_username }}
        <span v-if="orderInfo.status === 'pending'"> · 等待双方确认完成</span>
        <span v-else> · 已完成，可互评</span>
      </p>
      <div class="confirm-status">
        <span :class="orderInfo.publisher_confirmed ? 'ok' : 'pending'">
          发布者{{ orderInfo.publisher_confirmed ? '已确认' : '未确认' }}
        </span>
        <span :class="orderInfo.acceptor_confirmed ? 'ok' : 'pending'">
          接单者{{ orderInfo.acceptor_confirmed ? '已确认' : '未确认' }}
        </span>
      </div>
      <button
        v-if="orderInfo.can_confirm"
        class="btn"
        @click="confirmComplete"
      >确认任务已完成</button>
      <button
        v-if="orderInfo.can_revoke"
        class="btn btn-revoke"
        @click="revokeTask"
      >撤销帖子</button>
    </div>

    <div v-if="orderInfo && orderInfo.can_review" class="detail-section review-section">
      <div class="section-title">评价 {{ orderInfo.review_target_username }}</div>
      <p class="review-hint">订单已完成，请为对方打分（1-5 星），评价将影响信用分。</p>
      <div class="star-row">
        <button
          v-for="n in 5"
          :key="n"
          type="button"
          class="star-btn"
          :class="{ active: reviewForm.rating >= n }"
          @click="reviewForm.rating = n"
        >★</button>
      </div>
      <textarea
        v-model="reviewForm.comment"
        class="review-input"
        placeholder="选填：说说合作体验"
        rows="3"
      />
      <button class="btn" @click="submitReview">提交评价</button>
    </div>

    <div v-if="orderInfo && orderInfo.my_review" class="detail-section review-done">
      <div class="section-title">我的评价</div>
      <p class="section-content">
        已对 {{ orderInfo.review_target_username }} 评分：
        <strong>{{ orderInfo.my_review.rating }} 星</strong>
        <span v-if="orderInfo.my_review.comment"> — {{ orderInfo.my_review.comment }}</span>
      </p>
    </div>

    <div class="detail-actions">
      <button
        v-if="logged && !isMyTask"
        class="btn"
        :class="{ 'btn-disabled': !canAccept }"
        :disabled="!canAccept"
        @click="accept"
      >{{ acceptButtonText }}</button>
      <button
        v-else-if="logged && isMyTask && canRevoke"
        class="btn btn-revoke"
        @click="revokeTask"
      >撤销帖子</button>
      <div class="hint-text" v-else-if="!logged">请登录后接单，或返回帖子列表浏览更多任务。</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      task: {},
      me: null,
      logged: false,
      reviewForm: { rating: 5, comment: '' },
    }
  },
  computed: {
    orderInfo() {
      return this.task.order_info || null
    },
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
      return this.task.status === 'active' && this.logged && !this.isMyTask
    },
    isMyTask() {
      return !!(this.me?.id && this.task.publisher?.id === this.me.id)
    },
    canRevoke() {
      return this.orderInfo?.can_revoke === true
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
    publisherCreditText() {
      const credit = this.task.publisher?.credit_score
      if (credit == null || credit === '') return '未公开'
      const num = Number(credit)
      return Number.isFinite(num) ? num.toFixed(1) : String(credit)
    },
    deadlineText() {
      return this.task.deadline || '未设置'
    },
  },
  async mounted() {
    this.logged = !!localStorage.getItem('access')
    if (this.logged) {
      try {
        const r = await axios.get('/api/users/me/')
        this.me = r.data
      } catch (e) {
        this.me = null
      }
    }
    await this.loadTask()
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
        alert(this.errorMessage(e, '接单失败，请重试'))
        await this.loadTask()
      }
    },
    async confirmComplete() {
      if (!this.orderInfo?.can_confirm) return
      try {
        await axios.post(`/api/orders/${this.orderInfo.order_id}/confirm/`, {
          as_role: this.orderInfo.my_role,
        })
        alert('已确认完成')
        await this.loadTask()
      } catch (e) {
        alert(this.errorMessage(e, '确认失败'))
        await this.loadTask()
      }
    },
    async revokeTask() {
      if (!this.canRevoke) return
      if (!confirm(
        `确定撤销「${this.task.title}」吗？\n将取消当前接单，帖子恢复为「进行中」，其他人可重新接单。`
      )) return
      try {
        await axios.post(`/api/tasks/${this.task.id}/revoke/`)
        alert('已撤销，帖子已恢复为进行中')
        await this.loadTask()
      } catch (e) {
        alert(this.errorMessage(e, '撤销失败，请重试'))
        await this.loadTask()
      }
    },
    async submitReview() {
      if (!this.orderInfo?.can_review) return
      if (!this.reviewForm.rating) {
        alert('请选择评分')
        return
      }
      try {
        await axios.post('/api/reviews/', {
          order: this.orderInfo.order_id,
          rating: this.reviewForm.rating,
          comment: this.reviewForm.comment.trim(),
        })
        alert('评价成功，对方信用分已更新')
        await this.loadTask()
      } catch (e) {
        alert(this.errorMessage(e, '评价失败'))
      }
    },
    errorMessage(e, fallback) {
      const data = e.response?.data
      if (!data) return fallback
      if (typeof data.detail === 'string') return data.detail
      if (typeof data === 'object') {
        return Object.entries(data).map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(' ') : v}`).join('\n')
      }
      return fallback
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
.publisher-link {
  color: #2563eb;
  text-decoration: none;
}
.publisher-link:hover {
  text-decoration: underline;
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
.btn-revoke {
  background: #fff7ed;
  color: #c2410c;
  border: 1px solid #fed7aa;
}
.btn-revoke:hover {
  background: #ffedd5;
}
.btn-disabled,
.btn:disabled {
  background: #cbd5e1 !important;
  color: #64748b !important;
  cursor: not-allowed;
  box-shadow: none;
}
.order-section {
  background: #f0f9ff;
  border: 1px solid #bae6fd;
  border-radius: 12px;
  padding: 16px 18px;
}
.order-meta {
  margin: 0 0 12px;
  color: #334155;
  font-size: 0.95rem;
}
.confirm-status {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 14px;
  font-size: 0.9rem;
}
.confirm-status .ok {
  color: #166534;
  font-weight: 600;
}
.confirm-status .pending {
  color: #64748b;
}
.review-section {
  background: #faf5ff;
  border: 1px solid #e9d5ff;
  border-radius: 12px;
  padding: 16px 18px;
}
.review-hint {
  margin: 0 0 12px;
  color: #64748b;
  font-size: 0.9rem;
}
.star-row {
  display: flex;
  gap: 6px;
  margin-bottom: 12px;
}
.star-btn {
  border: none;
  background: transparent;
  font-size: 28px;
  color: #cbd5e1;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}
.star-btn.active {
  color: #f59e0b;
}
.review-input {
  width: 100%;
  box-sizing: border-box;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 10px 12px;
  margin-bottom: 12px;
  font-size: 15px;
  resize: vertical;
}
.review-done {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 12px;
  padding: 16px 18px;
}
</style>
