<template>
  <div class="card">
    <h3>发布任务</h3>

    <div class="form-row">
      <select v-model="form.category">
        <option value="carpool">拼车</option>
        <option value="errand">跑腿</option>
        <option value="agency">代办</option>
        <option value="emergency">特需</option>
      </select>
      <input v-model="form.title" placeholder="标题（简短清晰）" />
    </div>

    <div class="form-row">
      <input v-model="form.location" placeholder="位置（例如：浙江大学华家池）" />
      <input v-model="form.time" placeholder="时间（可选）" />
    </div>

    <div class="form-row">
      <textarea v-model="form.remark" rows="4" placeholder="备注 / 详细说明（可填写联系方式、特殊要求等）" style="flex:1"></textarea>
    </div>

    <div style="display:flex;justify-content:flex-end;gap:8px;margin-top:8px">
      <button class="btn ghost" @click="$router.back()">取消</button>
      <button class="btn" @click="publish">发布</button>
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
        time: '',
        remark: ''
      }
    }
  },
  methods: {
    async publish() {
      if (!this.form.title.trim()) { alert('请填写标题'); return }
      try {
        const token = localStorage.getItem('access')
        if (!token) { alert('请先登录'); return }
        await axios.post('/api/tasks/', this.form, { headers: { Authorization: 'Bearer ' + token } })
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
