<template>
	<view>
		<view class="example-body">
			<view class="uni-padding-wrap uni-common-mt uni-binding">
				<form @reset="formReset" class="form-box reg-box">
					<view class="regTitle">
						欢迎
						<span class="colTip">注册</span>
						律师在线
					</view>
					<view class="checkBox">
						<radio-group name="gender" @change="radioChange">
							<label>
								<radio value="1" checked="true" />
								普通用户
							</label>
							<label>
								<radio value="2" />
								律师用户
							</label>
						</radio-group>
					</view>
					<view class="uni-form-item uni-column">
						<span class="title">手机号码</span>
						<input class="uni-input" name="input" v-model="formData.mobile" placeholder="请输入手机号" @input="getValue" data-id="1" />
					</view>
					<view class="uni-form-item uni-column">
						<span class="title">密码</span>
						<input class="uni-input" type="password" name="input" placeholder="请输入密码" @input="getValue" data-id="2" />
					</view>
					<view class="uni-form-item uni-column" v-if="isLawyer">
						<span class="title">律师营业执照号</span>
						<input class="uni-input" name="input" placeholder="请输入律师营业执照号" @input="getValue" data-id="3" />
					</view>
					<view class="uni-form-item uni-column">
						<span class="title">验证码</span>
						<input class="uni-input" name="input" placeholder="验证码" @input="getValue" data-id="4" />
						<span class="code">
							<span @click="getCode" v-show="disabled" class="get-vcode">{{ countdown }}</span>
							<text v-show="timestatus">{{ times }}秒重获</text>
						</span>
					</view>
				</form>
			</view>
		</view>
		<view class="uni-btn-v"><button type="primary" @click="formSubmit">注册</button></view>
	</view>
</template>

<script>
import { code, reg } from '@/api/login.js';
import helper from '../../common/util.js';
export default {
	name: 'binding',
	components: {},
	data() {
		return {
			formData: {
				mobile: '',
				password: '',
				expert_ident: '',
				code: ''
			},
			countdown: '获取验证码',
			times: 60,
			disabled: true,
			timestatus: false,
			clear: '',
			isLawyer: false
		};
	},
	onLoad(val) {
		this.formData.mobile=val.mobile
	},
	methods: {
		formSubmit: function(e) {
			// console.log(this.isLawyer);
			var that = this;
			if (!this.isLawyer) {
				delete this.formData.expert_ident;
				// Vue.delete(that.formData,'expert_ident');//vue方法
			}
			console.log(this.isLawyer)
			if (that.formData.mobile === '') {
				uni.showToast({
					title: '请输入手机号码',
					icon: 'none'
				});
			} else if (!helper.c_mobile.test(that.formData.mobile)) {
				uni.showToast({
					title: '手机号码错误',
					icon: 'none'
				});
			} else if (that.formData.password === '') {
				uni.showToast({
					title: '请输入密码',
					icon: 'none'
				});
			} 
			else if (!helper.reg.test(that.formData.password)) {
				uni.showToast({
					title: '密码必须是3到9位数字字母下划线',
					icon: 'none'
				});
			} 
			else if (that.formData.code === '') {
				uni.showToast({
					title: '请输入验证码',
					icon: 'none'
				});
			} 
			else if (that.formData.expert_ident === '') {
				uni.showToast({
					title: '请输入律师执业证号',
					icon: 'none'
				});
			}
			else {
				console.log(this.formData);
				reg(that.formData)
					.then(res => {
						console.log(res);
						if (res.statusCode === 201) {
							uni.navigateTo({
								url: '/pages/user/login'
							});
						}
					})
					.catch(err => {
						console.log('form发生了submit事件，携带数据为：' + JSON.stringify(e.detail.value));
					});
			}
		},

		// 获取input内容   (ps 现在uniapp可以用vue的双向绑定来获取input的值)
		getValue(event) {
			var that = this;
			var value = event.detail.value; //获取触发的值
			var id = event.currentTarget.dataset.id; //获取自定义的数值做判断
			if (id == 1) {
				that.formData.mobile = value;
			} else if (id == 2) {
				that.formData.password = value;
			} else if (id == 3) {
				that.formData.expert_ident = value;
			} else {
				that.formData.code = value;
			}
		},
		// 获取验证码
		getCode() {
			var that = this;
			if (that.formData.mobile === '') {
				uni.showToast({
					title: '请输入手机号码',
					icon: 'none'
				});
			} else if (!helper.c_mobile.test(that.formData.mobile)) {
				uni.showToast({
					title: '手机号码错误',
					icon: 'none'
				});
			} else {
				code(this.formData.mobile)
					.then(res => {
						uni.showToast({
							title: '验证码发送成功',
							icon: 'none'
						});
						that.disabled = false; //禁用点击
						that.times = 60;
						that.timestatus = true;
						that.clear = setInterval(that.countDown, 1000);
					})
					.catch(err => {});
			}
		},
		// 倒计时
		countDown() {
			var that = this;
			if (!that.times) {
				that.disabled = true;
				that.timestatus = false;
				that.countdown = '获取验证码';
				clearInterval(that.clear);
			} else {
				--that.times;
			}
		},
		// 用户选择
		radioChange: function(e) {
			if (e.detail.value === '1') {
				this.isLawyer = false;
			} else {
				this.isLawyer = true;
			}
		}
	}
};
</script>

<style></style>
