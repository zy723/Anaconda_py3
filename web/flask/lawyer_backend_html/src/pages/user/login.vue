<template>
	<view>
		<view class="example-body">
			<view class="uni-padding-wrap uni-common-mt uni-binding">
				<form @reset="formReset" class="form-box">
					<view class="uni-form-item uni-column">
						<span class="title">手机号码</span>
						<input class="uni-input" name="input" placeholder="请输入手机号" @input="getValue" data-id="1" />
					</view>
					<view class="uni-form-item uni-column">
						<span class="title">密码</span>
						<input class="uni-input" type="password" name="input" placeholder="请输入密码" @input="getValue" data-id="2" />
						<!-- 暂时保留验证码登录 -->
						<!-- <input class="uni-input" name="input" placeholder="验证码" @input="getValue" data-id="2" /> -->
						<!-- <span class="code">
							<button @click="getCode" :disabled="disabled" class="get-vcode">
								{{ countdown }}
								<text v-show="timestatus">秒重获</text>
							</button>
							<span @click="getCode" v-show="disabled" class="get-vcode">{{ countdown }}</span>
							<text v-show="timestatus">{{ times }}秒重获</text>
						</span> -->
					</view>
				</form>
			</view>
		</view>
		<view class="uni-btn-v"><button type="primary" @click="formSubmit">绑定</button></view>
	</view>
</template>

<script>
import { login } from '@/api/login.js';
import helper from '../../common/util.js';
export default {
	name: 'binding',
	components: {},
	data() {
		return {
			password: '',
			mobile: '',
			countdown: '获取验证码',
			times: 60,
			disabled: true,
			timestatus: false,
			clear: ''
		};
	},
	methods: {
		// 提交表单
		formSubmit: function(e) {
			var that = this;
			if (that.mobile === '') {
				uni.showToast({
					title: '请输入手机号码',
					icon: 'none'
				});
			} else if (!helper.c_mobile.test(that.mobile)) {
				uni.showToast({
					title: '手机号码错误',
					icon: 'none'
				});
			} else if (that.password === '') {
				uni.showToast({
					title: '请输入验证码',
					icon: 'none'
				});
			} else {
				login({
					mobile: that.mobile,
					password: that.password
				})
					.then(res => {
						if (res.statusCode === 400) {
							uni.navigateTo({
								url: '/pages/user/reg?mobile='+that.mobile
							});
						} else if (res.statusCode === 401) {
							uni.showToast({
								title: '密码错误',
								icon: 'none'
							});
						} else {
							uni.setStorage({ key: 'access_token', data: res.data.token });
							uni.navigateTo({
								url: '/pages/index/index'
							});
						}
					})
					.catch(err => {
						console.log('form发生了submit事件，携带数据为：' + JSON.stringify(e.detail.value));
					});
			}
		},

		// 获取input内容   （ps 现在uniapp可以用vue的双向绑定来获取input的值）
		getValue(event) {
			var that = this;
			var value = event.detail.value; //获取触发的值
			var id = event.currentTarget.dataset.id; //获取自定义的数值做判断
			if (id == 1) {
				that.mobile = value;
			} else {
				that.password = value;
			}
		},
		// 获取验证码
		// 暂时保留此功能
		getCode() {
			var that = this;
			if (that.mobile === '') {
				uni.showToast({
					title: '请输入手机号码',
					icon: 'none'
				});
			} else if (!helper.c_mobile.test(that.mobile)) {
				uni.showToast({
					title: '手机号码错误',
					icon: 'none'
				});
			} else {
				that.disabled = false; //禁用点击
				that.times = 60;
				that.timestatus = true;
				that.clear = setInterval(that.countDown, 1000);
			}
		},
		// 倒计时
		// 暂时保留此功能
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
		}
	}
};
</script>

<style></style>
