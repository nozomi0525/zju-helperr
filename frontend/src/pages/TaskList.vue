<template>
  <div>
    <div class="card list-header-card">
      <div class="card-header">
        <h3>任务列表</h3>
        <div class="subtitle">筛选你感兴趣的任务，及时查看最新发布的帖子</div>
      </div>
      <div class="form-row">
        <select v-model="category">
          <option value="">全部分类</option>
          <option value="carpool">拼车</option>
          <option value="errand">跑腿</option>
          <option value="agency">代办</option>
          <option value="emergency">特需</option>
          <option value="other">其他</option>
        </select>
        <select v-model="paidFilter">
          <option value="">全部付费类型</option>
          <option value="paid">有偿</option>
          <option value="free">无偿</option>
        </select>
        <button class="btn primary" @click="load" title="筛选当前条件">筛选</button>
      </div>
    </div>

    <div class="card empty-state" v-if="tasks.length === 0">暂无任务，稍后再试或点击刷新</div>

    <div class="card task-card" v-for="t in tasks" :key="t.id">
      <div class="task-item">
        <div class="task-meta">
          <div class="task-title">{{ t.title }}</div>
          <div class="task-info">
            {{ categoryText(t.category) }} · {{ t.location || '未知地点' }} ·
            <span :class="['status-chip', statusClass(t.status)]">{{ statusText(t.status) }}</span>
          </div>
          <p v-if="t.remark" class="task-desc">{{ t.remark }}</p>
        </div>
        <div class="task-actions">
          <router-link :to="`/task/${t.id}`" class="btn ghost">查看详情</router-link>
          <button
            v-if="logged"
            class="btn"
            :class="{ 'btn-disabled': !canAccept(t) }"
            :disabled="!canAccept(t)"
            @click="accept(t)"
          >{{ acceptButtonText(t) }}</button>
        </div>
      </div>
      <div class="task-footer">
        <span class="pill">类别：{{ categoryText(t.category) }}</span>
        <span class="tag">状态：{{ statusText(t.status) }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      tasks: [],
      category: '',
      paidFilter: '',
      logged: false
    }
  },
  methods: {
    categoryText(category) {
      if (!category) return '未知'
      if (category === 'carpool') return '拼车'
      if (category === 'errand') return '跑腿'
      if (category === 'agency') return '代办'
      if (category === 'emergency') return '特需'
      if (category === 'other') return '其他'
      return category
    },
    statusText(status) {
      if (!status) return '未知状态'
      if (status === 'active') return '进行中'
      if (status === 'accepted') return '已接单'
      if (status === 'completed') return '已完成'
      if (status === 'expired') return '已过期'
      return status
    },
    statusClass(status) {
      if (status === 'active') return 'status-active'
      if (status === 'accepted') return 'status-accepted'
      if (status === 'completed') return 'status-completed'
      if (status === 'expired') return 'status-expired'
      return 'status-default'
    },
    canAccept(t) {
      return t.status === 'active'
    },
    acceptButtonText(t) {
      if (t.status === 'accepted') return '已接单'
      if (t.status === 'completed') return '已完成'
      if (t.status === 'expired') return '已过期'
      return '接单'
    },
    async load() {
      // build query params for category and paid filter
      const params = new URLSearchParams()
      if (this.category) params.append('category', this.category)
      // include is_paid param when selected to let backend filter if supported
      if (this.paidFilter === 'paid') params.append('is_paid', 'true')
      if (this.paidFilter === 'free') params.append('is_paid', 'false')

      const url = '/api/tasks/' + (params.toString() ? ('?' + params.toString()) : '')
      const r = await axios.get(url)
      this.tasks = r.data

      // Apply client-side filters to guarantee correct results even if backend ignores params
      if (this.category) {
        this.tasks = this.tasks.filter(t => t.category === this.category)
      }
      if (this.paidFilter === 'paid') this.tasks = this.tasks.filter(t => !!t.is_paid)
      if (this.paidFilter === 'free') this.tasks = this.tasks.filter(t => !t.is_paid)
    },
    async accept(t) {
      if (!this.canAccept(t)) return
      try {
        if (!localStorage.getItem('access')) {
          alert('请先登录')
          return
        }
        await axios.post('/api/orders/', { task: t.id })
        alert('接单成功')
        await this.load()
      } catch (e) {
        const msg = e.response?.data?.detail
          || (e.response?.data && Object.values(e.response.data).flat().join(' '))
          || '接单失败，请重试'
        alert(msg)
        await this.load()
      }
    }
  },
  mounted() {
    this.load()
    this.logged = !!localStorage.getItem('access')
  }
}
</script>

<style scoped>
.list-header-card {
  margin-bottom: 18px;
  background: #ffffff;
}
.card-header {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 16px;
}
.card-header h3 {
  margin: 0;
  color: #0f172a;
  font-size: 1.4rem;
}
.subtitle {
  margin: 0;
  color: #64748b;
  font-size: 0.95rem;
}
.form-row {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: center;
}
.form-row select {
  min-width: 160px;
  padding: 10px 14px;
  border: 1px solid #cbd5e1;
  border-radius: 12px;
  background: #f8fafc;
  color: #0f172a;
}
.btn.primary {
  background: #4338ca;
  color: white;
}
.task-card {
  border: 1px solid #e2e8f0;
  border-radius: 18px;
  margin-bottom: 16px;
  overflow: hidden;
  box-shadow: 0 8px 28px rgba(15, 23, 42, 0.04);
}
.task-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  padding: 22px 22px 14px;
}
.task-meta {
  min-width: 0;
}
.task-title {
  font-weight: 700;
  color: #0f172a;
  font-size: 1.06rem;
  line-height: 1.5;
}
.task-info {
  margin-top: 8px;
  color: #64748b;
  font-size: 0.94rem;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.task-desc {
  margin: 12px 0 0;
  color: #334155;
  line-height: 1.7;
  max-width: 720px;
}
.status-chip {
  padding: 5px 11px;
  border-radius: 999px;
  font-size: 0.82rem;
  font-weight: 600;
  white-space: nowrap;
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
.task-actions {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}
.task-actions .btn {
  min-width: 84px;
}
.task-actions .ghost {
  background: transparent;
  border: 1px solid #cbd5e1;
  color: #0f172a;
}
.task-footer {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
  padding: 14px 20px 18px;
  background: #f8fafc;
}
.pill,
.tag {
  display: inline-flex;
  padding: 6px 14px;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 600;
}
.pill {
  background: #eef2ff;
  color: #3730a3;
}
.tag {
  background: #f1f5f9;
  color: #475569;
}
.btn-disabled,
.btn:disabled {
  background: #cbd5e1 !important;
  color: #64748b !important;
  cursor: not-allowed;
  box-shadow: none;
}
.empty-state {
  text-align: center;
  color: #475569;
  padding: 28px 0;
  border: 1px dashed #cbd5e1;
  border-radius: 16px;
  background: #f8fafc;
}
@media (max-width: 760px) {
  .task-item {
    flex-direction: column;
    align-items: stretch;
  }
  .task-actions {
    justify-content: flex-end;
    width: 100%;
  }
}
</style>
