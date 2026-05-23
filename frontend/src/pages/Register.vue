<template>
  <div id="register-page-wrapper" class="register-page">
    <div class="register-card">
      <h3 class="register-title">注册</h3>

      <div class="register-form-row">
        <input v-model="username" placeholder="用户名" />
      </div>

      <div class="register-form-row">
        <input type="password" v-model="password" placeholder="密码" />
      </div>

      <!-- 用户须知区域：插入于表单底部，注册按钮上方 -->
      <div class="register-form-row user-notice-wrapper">
        <div class="user-notice" aria-label="用户须知">
          <p class="user-notice-title">【重要提示】本须知包含责任限制及个人信息处理条款，请仔细阅读。注册、登录或使用本平台，即视为用户已阅读并同意全部条款。</p>
          <div class="user-notice-body">
            <p>一、账号与注册</p>
            <p>·仅限本校在校学生及教职工注册。本平台为免费校园互助平台，不收取任何费用。</p>
            <p>·请妥善保管账号密码，禁止转借、出租或出售。因保管不当导致的损失由用户自行承担。</p>
            <p>二、行为规范</p>
            <p>·严格遵守法律法规及校规校纪，禁止利用平台从事违法违规活动。</p>
            <p>·秉持诚信友善，禁止发布虚假信息、恶意骚扰、欺诈或刷量。</p>
            <p>·发布内容须符合公序良俗，禁止违法违规、侮辱诽谤、色情暴力、泄露敏感信息等内容。</p>
            <p>·禁止攻击系统、盗用他人信息或使用第三方插件干扰平台运行。</p>
            <p>三、服务与免责</p>
            <p>·本平台仅提供校园互助信息对接服务，不参与互助行为本身。</p>
            <p>·平台对用户信息真实性不作实质性担保，但将依法履行必要管理义务。用户间互助纠纷由双方自行解决。</p>
            <p>·因不可抗力、网络故障、你自身操作失误或违规使用导致的损失，运营方不承担赔偿责任。</p>
            <p>·平台包含的第三方服务，相关纠纷由用户与第三方自行解决。</p>
            <p>四、个人信息保护</p>
            <p>·平台遵循最小必要原则收集信息，仅用于身份核验、互助对接及安全保障，不用于商业营销或向第三方出售。</p>
            <p>·运营方采取合理安全措施保护个人信息。除法律法规要求或经用户同意外，不向无关第三方提供。</p>
            <p>·因不可抗力或用户自身原因导致的信息泄露，运营方不承担责任。</p>
            <p>五、其他</p>
            <p>·本须知可适时修改，修改后继续使用即视为同意。</p>
            <p>·违规用户须承担赔偿责任，运营方保留追究法律责任的权利。</p>
            <p>·本须知自发布之日起生效，未尽事宜按法律法规执行。</p>
          </div>
        </div>

        <label class="agree-row">
          <input type="checkbox" v-model="agreed" />
          <span class="agree-text">我已阅读并同意上述用户须知</span>
        </label>
      </div>

      <div class="register-actions">
        <button class="register-btn" :disabled="!agreed" @click="register">注册</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data(){return {username:'',password:'',agreed:false}},
  methods:{
    async register(){
      if(!this.agreed){
        alert('请阅读并同意用户须知后再注册')
        return
      }
      try{
        console.log('Register attempt', {username: this.username, agreed: this.agreed})
        const payload = {username:this.username,password:this.password,agreed:this.agreed}
        const r = await axios.post('/api/users/',payload)
        console.log('Register response', r.status, r.data)
        alert('注册成功，请登录')
        this.$router.push('/login')
      }catch(e){
        console.error('Register error', e)
        let msg = '注册失败'
        if(e.response && e.response.data){
          const data = e.response.data
          if(typeof data === 'string') msg = data
          else if(data.detail) msg = data.detail
          else {
            msg = Object.entries(data).map(([k,v]) => `${k}: ${Array.isArray(v)?v.join(' '):v}`).join('\n')
          }
        }
        alert(msg)
      }
    }
  }
}
</script>

<style>
/* Match the visual style used by Login/Profile but scoped to Register page */
#register-page-wrapper.register-page {
  min-height: 100vh;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  padding: 20px;
  box-sizing: border-box;
}

#register-page-wrapper .register-card {
  background: #ffffff !important;
  border-radius: 16px !important;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1) !important;
  padding: 40px 30px !important;
  width: 100% !important;
  max-width: 400px !important;
  text-align: center !important;
}

#register-page-wrapper .register-title {
  margin: 0 0 30px !important;
  font-size: 28px !important;
  font-weight: 600 !important;
  color: #333 !important;
}

#register-page-wrapper .register-form-row {
  margin-bottom: 20px !important;
}

#register-page-wrapper .register-form-row input {
  width: 100% !important;
  padding: 14px 16px !important;
  font-size: 16px !important;
  border: 1px solid #ddd !important;
  border-radius: 10px !important;
  outline: none !important;
  transition: border-color 0.3s, box-shadow 0.3s !important;
  background: #fafafa !important;
}

#register-page-wrapper .register-form-row input:focus {
  border-color: #667eea !important;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15) !important;
  background: #fff !important;
}

#register-page-wrapper .register-actions {
  display: flex !important;
  gap: 12px !important;
  align-items: center !important;
  margin-top: 10px !important;
}

#register-page-wrapper .register-btn {
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

#register-page-wrapper .register-btn:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 18px rgba(102, 126, 234, 0.5) !important;
}

#register-page-wrapper .register-btn:active {
  transform: translateY(0) !important;
}

#register-page-wrapper .user-notice-wrapper {
  margin-bottom: 12px !important;
  text-align: left !important;
}

#register-page-wrapper .user-notice {
  border: 1px solid #eee !important;
  background: #fafafa !important;
  padding: 12px !important;
  border-radius: 10px !important;
}

#register-page-wrapper .user-notice-title {
  margin: 0 0 8px 0 !important;
  font-weight: 600 !important;
  color: #333 !important;
  font-size: 14px !important;
}

#register-page-wrapper .user-notice-body {
  max-height: 200px !important;
  overflow: auto !important;
  padding-right: 6px !important;
  font-size: 13px !important;
  color: #444 !important;
  line-height: 1.5 !important;
}

#register-page-wrapper .agree-row {
  display: flex !important;
  align-items: center !important;
  gap: 8px !important;
  margin-top: 10px !important;
}

#register-page-wrapper .agree-row input[type="checkbox"] {
  width: 16px !important;
  height: 16px !important;
}

#register-page-wrapper .agree-text {
  font-size: 14px !important;
  color: #333 !important;
}

#register-page-wrapper .register-btn[disabled] {
  opacity: 0.5 !important;
  cursor: not-allowed !important;
  transform: none !important;
  box-shadow: none !important;
}
</style>
