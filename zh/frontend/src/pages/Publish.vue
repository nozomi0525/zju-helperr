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
      <input v-model="form.title" placeholder="标题" />
    </div>
    <div class="form-row">
      <input v-model="form.location" placeholder="位置" />
      <input v-model="form.remark" placeholder="备注" />
    </div>
    <div>
      <button class="btn" @click="publish">发布</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data(){return {form:{category:'carpool',title:'',location:'',remark:''}}},
  methods:{
    async publish(){
      try{
        const token=localStorage.getItem('access')
        if(!token){alert('请先登录');return}
        await axios.post('/api/tasks/',this.form,{headers:{Authorization:'Bearer '+token}})
        alert('发布成功')
        this.$router.push('/')
      }catch(e){alert('发布失败')}
    }
  }
}
</script>
