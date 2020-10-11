<template>
	<view>
		<uni-nav-bar left-icon="arrowleft" title="个人主页" @click-left="back" class="homeList" :color="color" />
		<!-- head -->
		<view class="userHeader">
			
			<!-- 信息 -->
			<view class="userHeadeBox">
				<view class="uni-padding-wrap" @click="handleUser">
					<view class="headerPic">
						<image src="../../../static/image/img1.png" v-if="baseData.user_photo_url === null"></image>
						<image :src="baseData.user_photo_url" v-else></image>
					</view>
					<view class="infoText">
						{{ baseData.user_name }}
						<i class="iconfont">&#xe615;</i>
					</view>
				</view>
			</view>
			<!-- end -->
			<view class="userInfoTip">
				<view @click="handleAttention">
					<p><i class="iconHot attention"></i></p>
					<p>关注律师</p>
				</view>
				<view>
					<router-link to="/pages/template/my-ask/ask-list">
						<p><i class="iconHot askicon"></i></p>
						<p>我的提问</p>
					</router-link>
				</view>
				<view>
					<router-link to="/pages/template/my-advisory/consult-list">
						<p><i class="iconHot consulticon"></i></p>
						<p>我的咨询</p>
					</router-link>
				</view>
				<view>
					<router-link to="/pages/template/my-advisory/my-evaluatelist">
						<p><i class="iconHot comicon"></i></p>
						<p>我的评价</p>
					</router-link>
				</view>
			</view>
		</view>
		<!-- end -->
		<view class="userBox">
			<view class="example-infobox example-body">
				<view>
					<view class="uni-padding-wrap uni-common-mt">
						<view class="userList">
							<uni-list>
								<uni-list-item thumb="../../../static/image/icon7.png" title="我的订单" />
								<uni-list-item thumb="../../../static/image/icon8.png" title="智能客服" />
								<uni-list-item thumb="../../../static/image/icon9.png" :show-badge="true" title="系统消息" badge-text="12" />
							</uni-list>
						</view>
					</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
import uniNavBar from '@/components/uni-nav-bar/uni-nav-bar.vue';
import uniList from '@/components/uni-list/uni-list.vue';
import uniListItem from '@/components/uni-list-item/uni-list-item.vue';
import { userInfo, token } from '@/api/user.js';
export default {
	components: { uniNavBar, uniList, uniListItem },
	data() {
		return {
			height: '44px',
			payShow: false,
			baseData: {}
		};
	},
	// 监听页面加载，为上个页面传递的数据，用于页面传参
	onLoad() {
		this.getData();
	},
	methods: {
		// 返回
		back() {
			uni.navigateBack({
				delta: 1
			});
		},
		// 个人中心信息
		getData() {
			userInfo()
				.then(res => {
					if (res.statusCode === 200) {
						this.baseData = res.data;
						token()
							.then(obj => {
								console.log(obj);
							})
							.catch(err => {});
					}
					if (res.statusCode === 401) {
						// uni.navigateTo({
						// 	url: '/pages/user/login'
						// });
						token()
							.then(obj => {
								console.log(obj);
							})
							.catch(err => {});
					}
				})
				.catch(err => {});
		},
		// 修改个人中心
		handleUser: function(e) {
			uni.navigateTo({
				url: '/pages/template/user/userInfo'
			});
		},
		// 关注的律师
		handleAttention: function(e) {
			uni.navigateTo({
				url: '/pages/template/my-advisory/attention-list'
			});
		}
	}
};
</script>

<style>
page {
	display: flex;
	flex-direction: column;
	box-sizing: border-box;
	background-color: #efeff4;
}
</style>
