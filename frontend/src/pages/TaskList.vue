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
        </select>
        <select v-model="paidFilter">
          <option value="">全部付费类型</option>
          <option value="paid">有偿</option>
          <option value="free">无偿</option>
        </select>
        <select v-model="statusFilter">
          <option value="">全部状态</option>
          <option value="active">进行中</option>
          <option value="accepted">已接单</option>
          <option value="completed">已完成</option>
        </select>
        <button class="btn primary" @click="load" title="筛选当前条件">筛选</button>
        <button
          class="btn"
          :class="{ 'btn-mine-active': showMineOnly }"
          @click="toggleMineFilter"
          title="只显示我发布的帖子"
        >我的发布</button>
        <button class="btn" @click="refreshAll" title="清空筛选并刷新任务列表">刷新</button>
      </div>
    </div>

    <div class="card empty-state" v-if="tasks.length === 0">暂无任务，稍后再试或点击刷新</div>

    <div
      class="card task-card"
      v-for="t in tasks"
      :key="t.id"
      :class="{ 'task-card-mine': t.is_my_accepted }"
    >
      <div class="task-item">
        <div class="task-meta">
          <div class="task-title-row">
            <div class="task-title">{{ t.title }}</div>
            <span v-if="t.is_my_accepted" class="my-order-badge">我的接单</span>
          </div>
          <div class="task-info task-location">
            <span class="location-label">地址：</span>{{ t.location || '未知地点' }}
          </div>
          <div class="task-meta-extra">
            <span class="meta-chip" :class="{ 'meta-chip-reward': t.is_paid }">{{ rewardText(t) }}</span>
            <span class="meta-chip">时间：{{ formatDate(t.deadline || t.created_at) }}</span>
          </div>
          <p v-if="t.remark" class="task-desc">{{ t.remark }}</p>
        </div>
        <div class="task-actions">
          <router-link :to="`/task/${t.id}`" class="btn ghost">查看详情</router-link>
          <template v-if="canManage(t)">
            <button class="btn btn-edit" @click="openEdit(t)">编辑</button>
            <button class="btn btn-danger" @click="removeTask(t)">删除</button>
          </template>
          <button
            v-if="logged && !isMyTask(t)"
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
        <span v-if="isMyTask(t)" class="tag tag-mine">我的发布</span>
      </div>
    </div>

    <div v-if="showEditModal" class="edit-modal-backdrop" @click.self="closeEdit">
      <div class="edit-modal card">
        <h3>编辑帖子</h3>
        <div class="edit-form-row">
          <select v-model="editForm.category">
            <option value="carpool">拼车</option>
            <option value="errand">跑腿</option>
            <option value="agency">代办</option>
            <option value="emergency">特需</option>
          </select>
        </div>
        <div class="edit-form-row">
          <input v-model="editForm.title" placeholder="标题" />
        </div>
        <div class="edit-form-row">
          <input v-model="editForm.location" placeholder="位置" />
        </div>
        <div class="edit-form-row">
          <input v-model="editForm.deadline" placeholder="时间" />
        </div>
        <div class="edit-form-row edit-payment-row">
          <label><input type="radio" value="free" v-model="editForm.payment" /> 无偿</label>
          <label><input type="radio" value="paid" v-model="editForm.payment" /> 有偿</label>
        </div>
        <div class="edit-form-row" v-if="editForm.payment === 'paid'">
          <input v-model="editForm.reward" placeholder="报酬描述" />
        </div>
        <div class="edit-form-row">
          <input v-model="editForm.remark" placeholder="任务说明" />
        </div>
        <div class="edit-form-row">
          <input v-model="editForm.contact_info" placeholder="联系方式（仅接单人可见）" />
        </div>
        <div class="edit-modal-actions">
          <button class="btn ghost" @click="closeEdit">取消</button>
          <button class="btn primary" @click="saveEdit">保存</button>
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
      tasks: [],
      category: '',
      paidFilter: '',
      statusFilter: '',
      showMineOnly: false,
      me: null,
      logged: false,
      showEditModal: false,
      editingTaskId: null,
      editForm: {
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
    isMyTask(t) {
      return this.logged && this.me?.id && t.publisher?.id === this.me.id
    },
    canManage(t) {
      return this.isMyTask(t) && t.status === 'active'
    },
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
    async fetchMe() {
      try {
        const r = await axios.get('/api/users/me/')
        this.me = r.data
      } catch (e) {
        this.me = null
        if (e.response?.status === 401) {
          localStorage.removeItem('access')
          localStorage.removeItem('refresh')
        }
      }
    },
    async toggleMineFilter() {
      // if enabling "mine" filter but not logged in, prompt to login
      if (!this.showMineOnly && !this.logged) {
        alert('请先登录以查看我的发布')
        return
      }
      this.showMineOnly = !this.showMineOnly
      if (this.showMineOnly && !this.me) {
        await this.fetchMe()
      }
      this.load()
    },
    async load() {
      // build query params for category and paid filter
      const params = new URLSearchParams()
      if (this.category) params.append('category', this.category)
      if (this.statusFilter) params.append('status', this.statusFilter)
      // include is_paid param when selected to let backend filter if supported
      if (this.paidFilter === 'paid') params.append('is_paid', 'true')
      if (this.paidFilter === 'free') params.append('is_paid', 'false')

      const url = '/api/tasks/' + (params.toString() ? ('?' + params.toString()) : '')
      const r = await axios.get(url)
      // ensure we have current user info when mine-only filter is active
      if (this.showMineOnly && !this.me) {
        await this.fetchMe()
      }
      this.tasks = this.applyFiltersAndSort(r.data)
    },
    async refreshAll() {
      this.category = ''
      this.paidFilter = ''
      this.statusFilter = ''
      const r = await axios.get('/api/tasks/')
      this.tasks = this.applyFiltersAndSort(r.data)
    },
    applyFiltersAndSort(list) {
      let tasks = list
      if (this.category) {
        tasks = tasks.filter(t => t.category === this.category)
      }
      if (this.statusFilter) {
        tasks = tasks.filter(t => t.status === this.statusFilter)
      }
      if (this.paidFilter === 'paid') tasks = tasks.filter(t => !!t.is_paid)
      if (this.paidFilter === 'free') tasks = tasks.filter(t => !t.is_paid)
      if (this.showMineOnly && this.me?.id) {
        tasks = tasks.filter(t => t.publisher?.id === this.me.id)
      }
      return this.sortMyAcceptedFirst(tasks)
    },
    sortMyAcceptedFirst(tasks) {
      if (!this.logged) return tasks
      return [...tasks].sort((a, b) => {
        const mineA = a.is_my_accepted ? 1 : 0
        const mineB = b.is_my_accepted ? 1 : 0
        if (mineB !== mineA) return mineB - mineA
        return new Date(b.created_at) - new Date(a.created_at)
      })
    },
    rewardText(t) {
      if (!t.is_paid) return '无偿'
      if (!t.reward) return '面议'
      const r = String(t.reward).trim()
      return /^\d+(\.\d+)?$/.test(r) ? `¥${r}` : r
    },
    formatDate(value) {
      if (!value) return '未知时间'
      const date = new Date(value)
      if (Number.isNaN(date.getTime())) return value
      return date.toLocaleString([], {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
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
    },
    async openEdit(t) {
      if (!this.canManage(t)) return
      try {
        const r = await axios.get(`/api/tasks/${t.id}/`)
        const task = r.data
        this.editingTaskId = task.id
        this.editForm = {
          category: task.category || 'carpool',
          title: task.title || '',
          location: task.location || '',
          deadline: task.deadline || '',
          payment: task.is_paid ? 'paid' : 'free',
          reward: task.reward || '',
          remark: task.remark || '',
          contact_info: task.contact_info || ''
        }
        this.showEditModal = true
      } catch (e) {
        alert('加载帖子失败，请重试')
      }
    },
    closeEdit() {
      this.showEditModal = false
      this.editingTaskId = null
    },
    async saveEdit() {
      if (!this.editForm.title.trim()) { alert('请填写标题'); return }
      if (!this.editForm.location.trim()) { alert('请填写地点'); return }
      if (!this.editForm.deadline) { alert('请填写时间'); return }
      if (this.editForm.payment === 'paid' && !this.editForm.reward.trim()) {
        alert('请选择有偿并填写报酬描述')
        return
      }
      if (!this.editForm.contact_info.trim()) {
        alert('请填写联系方式')
        return
      }
      try {
        const payload = {
          category: this.editForm.category,
          title: this.editForm.title,
          location: this.editForm.location,
          deadline: this.editForm.deadline,
          remark: this.editForm.remark,
          contact_info: this.editForm.contact_info.trim(),
          is_paid: this.editForm.payment === 'paid',
          reward: this.editForm.payment === 'paid' ? this.editForm.reward : ''
        }
        await axios.patch(`/api/tasks/${this.editingTaskId}/`, payload)
        alert('保存成功')
        this.closeEdit()
        await this.load()
      } catch (e) {
        const msg = e.response?.data?.detail
          || (e.response?.data && Object.entries(e.response.data).map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(' ') : v}`).join('\n'))
          || '保存失败，请重试'
        alert(msg)
      }
    },
    async removeTask(t) {
      if (!this.canManage(t)) return
      if (!confirm(`确定删除「${t.title}」吗？删除后无法恢复。`)) return
      try {
        await axios.delete(`/api/tasks/${t.id}/`)
        alert('已删除')
        await this.load()
      } catch (e) {
        const msg = e.response?.data?.detail
          || (e.response?.data && Object.values(e.response.data).flat().join(' '))
          || '删除失败，请重试'
        alert(msg)
      }
    }
  },
  mounted() {
    this.logged = !!localStorage.getItem('access')
    this.fetchMe().then(() => this.load())
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
.btn-mine-active {
  background: #2563eb;
  color: #ffffff;
  box-shadow: 0 1px 0 rgba(255, 255, 255, 0.12);
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
.task-title-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}
.task-title {
  font-weight: 700;
  color: #0f172a;
  font-size: 1.06rem;
  line-height: 1.5;
}
.my-order-badge {
  display: inline-flex;
  padding: 4px 10px;
  border-radius: 999px;
  background: #fef3c7;
  color: #b45309;
  font-size: 0.78rem;
  font-weight: 700;
}
.task-card-mine {
  border-color: #fcd34d;
  box-shadow: 0 8px 28px rgba(245, 158, 11, 0.12);
}
.task-info {
  margin-top: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.task-location {
  font-size: 1.04rem;
  color: #0f172a;
  font-weight: 700;
  background: #f8fafc;
  padding: 10px 14px;
  border-radius: 16px;
  border: 1px solid #dbeafe;
}
.location-label {
  color: #4338ca;
}
.task-desc {
  margin: 12px 0 0;
  color: #334155;
  line-height: 1.7;
  max-width: 720px;
}
.task-meta-extra {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.meta-chip {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 999px;
  background: #f1f5f9;
  color: #475569;
  font-size: 0.82rem;
  font-weight: 600;
}
.meta-chip-reward {
  background: #fef3c7;
  color: #b45309;
  font-weight: 700;
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
  font-family: inherit;
  font-size: 0.95rem;
  font-weight: 600;
  letter-spacing: 0.01em;
}
.task-actions .ghost {
  background: transparent;
  border: 1px solid #cbd5e1;
  color: #0f172a;
  text-decoration: none;
}
.task-actions .ghost:hover {
  text-decoration: none;
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
.tag-mine {
  background: #dbeafe;
  color: #1d4ed8;
}
.btn-edit {
  background: #eef2ff;
  color: #4338ca;
  border: 1px solid #c7d2fe;
}
.btn-danger {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
}
.btn-danger:hover {
  background: #fee2e2;
}
.edit-modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  z-index: 1000;
}
.edit-modal {
  width: 100%;
  max-width: 520px;
  max-height: 90vh;
  overflow-y: auto;
  padding: 24px;
  border-radius: 16px;
}
.edit-modal h3 {
  margin: 0 0 18px;
  color: #0f172a;
}
.edit-form-row {
  margin-bottom: 14px;
}
.edit-form-row input,
.edit-form-row select {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  font-size: 15px;
  box-sizing: border-box;
}
.edit-payment-row {
  display: flex;
  gap: 20px;
}
.edit-payment-row label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #334155;
}
.edit-modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 8px;
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
