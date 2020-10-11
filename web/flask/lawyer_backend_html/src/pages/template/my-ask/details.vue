<template>
	<view>
		<view class="example-box example-body">
			<view>
				<view class="uni-padding-wrap uni-common-mt">
					<view class="uni-list">
						<view class="uni-list-cell" hover-class="uni-list-cell-hover">
							<view class="uni-media-list">
								<view class="uni-media-list-body">
									<view class="uni-media-list-text-top">{{ baseData.qust_content.content }}</view>
									<view class="uni-media-list-text-bottom">
										<text class="fontColor999">{{ baseData.qustion.create_time }}</text>
										<text>
											<i class="iconfont iconTips fontColor333" @click="handleDel">&#xe61b;</i>
											<i class="iconfont iconTips fontColor333">&#xe61c;</i>
										</text>
									</view>
									<view class="fontCol666">{{ baseData.qustion.title }}</view>
									<!-- 相关图片暂时不做 -->
									<view class="uni-flex uni-row">
										<view class="flex-item"><image src="../../../static/image/pic1.jpg"></image></view>
										<view class="flex-item"><image src="../../../static/image/pic2.jpg"></image></view>
										<view class="flex-item"><image src="../../../static/image/pic3.jpg"></image></view>
									</view>
									<view class="uni-media-list-text-bottom">
										<text>
											<i class="iconfont iconTips">&#xe611;</i>
											<!-- <image src="../../static/image/icon1.png" class="iconTips"></image> -->
											{{ baseData.qustion.expertise }}
										</text>
										<text>{{ baseData.answer_list.length }}人回答</text>
									</view>
								</view>
							</view>
						</view>
					</view>
				</view>
			</view>
			<view class="titleInfo example-title ">
				相关回答
				<span class="title-line"></span>
			</view>
		</view>
		<!-- 弹层 -->

		<!-- 评论区 start -->
		<view class="uni-padding-wrap">
			<!-- 评论区 start -->
			<view class="">
				<view v-for="(value, index) in baseData.answer_list" :key="index" v-if="baseData.answer_list.length>0">
					<view class="uni-comment-list ask-list">
						<view class="uni-comment-face">
							<image :src="value.ans_photo_url" v-if="value.ans_photo_url !== null"></image>
							<image src="../../../static/image/img1.png"></image>
							<span class="vicon"></span>
						</view>
						<view class="uni-comment-body">
							<view class="uni-comment-top">
								<text>{{ value.ans_name }}</text>
								<text class="tip">答</text>
								<view class="rInfo">
									<button type="primary" size="mini" @click="handleFollow(value)" v-if="value.is_following === 0">关注</button>
									<button type="primary" size="mini" class="butFollow" @click="handleCancelFollow(value)" v-else>已关注</button>
									<button type="primary" size="mini" class="butConsult" v-if="value.paid_for_once === 0 && value.paid_for_hour === 0" @click="handleConsult(0)">
										付费咨询
									</button>
									<button type="primary" size="mini" class="butConsultFree" @click="handleConsult(1)" v-else>免费咨询</button>
								</view>
							</view>
							<view class="uni-media-list-text-time">
								<text>{{ value.create_time }}</text>
							</view>
							<view class="uni-comment-content">{{ value.content }}</view>
							<!-- 一期不做 -->
							<view class="chear">
								<span class="colBlue" @click="handleAsk(index)">追问</span>
								<view class="rInfo">
									<i class="iconfont">&#xe612;</i>
									<i class="iconfont">{{ value.fabulous }}266</i>
									
								</view>
							</view>
							<view class="uni-textarea textInfo" v-show="index === askShow"><textarea placeholder="我的追问" /></view>

							<view class="table-btn-view bttomBox" v-show="index === askShow"><button type="primary" @click="formSubmit">提交</button></view>
						</view>
					</view>
					<view class="uni-comment-list ask-list askBox">
						<view class="askCon">
							<view class="uni-comment-face">
								<image :src="value.ans_photo_url" v-if="value.ans_photo_url !== null"></image>
								<image src="../../../static/image/img1.png"></image>
								<span class="vicon"></span>
							</view>
							<view class="uni-comment-body">
								<view class="uni-comment-top">
									<text>{{ value.ans_name }}</text>
									<text class="tip">追问</text>
									<view class="rInfo"><i class="iconfont iconTips fontColor333" @click="handleDel">&#xe61b;</i></view>
								</view>
								<view class="uni-media-list-text-time">
									<text>{{ value.create_time }}</text>
								</view>
								<view class="askInfo">
									如果还有再次伤害呢？
								</view>
							</view>
						</view>
					</view>
				</view>
				<view class="example-body" v-else>
					<view class="noAskinfo">
						<i class=""></i>
						暂无咨询，快去
						<router-link to="/pages/template/my-ask/ask" class="colBlue">提问</router-link>
						吧！
					</view>
				</view>
			</view>
			<!-- 评论区 end -->
		</view>
		<!-- 评论区 end -->
		<span class="askIcon"><router-link to="/pages/template/my-ask/ask"><i></i>提问</router-link></span>
	</view>
</template>

<script>

import { homeDetails, following, cancelFollowing } from '@/api/index.js';
export default {
	components: {},
	data() {
		return {
			askShow: -1,
			parentId: null,
			baseData: []
		};
	},
	/**
	 * 当 searchInput 配置 disabled 为 true 时触发
	 */
	// 搜索框
	onNavigationBarSearchInputClicked(e) {
		console.log('事件执行了');
		uni.navigateTo({
			url: '/pages/template/nav-search-input/detail/detail'
		});
	},
	// 监听页面加载，为上个页面传递的数据，用于页面传参
	onLoad(options) {
		this.parentId = JSON.parse(options.id); // 字符串转对象
		this.getDetails();
	},
	methods: {
		// 获取详情信息
		getDetails: function() {
			homeDetails({ id: this.parentId })
				.then(res => {
					if (res.statusCode === 200) {
						this.baseData = res.data;
						
					}
				})
				.catch(err => {});
		},
		// 我要提问
		triggerCollapse: function() {
			uni.navigateTo({
				url: '/pages/template/my-ask/ask'
			});
		},
		// 个人中心
		handleUser: function() {
			uni.navigateTo({
				url: '/pages/template/user/user'
			});
		},
		// 关注
		handleFollow(val) {
			following({ lawyer_id: val.lawyer_id })
				.then(res => {
					if (res.statusCode === 200) {
						uni.showToast({
							title: '关注成功',
							icon: 'none'
						});
					} else if (res.statusCode === 401) {
						uni.navigateTo({
							url: '/pages/user/login'
						});
					}
				})
				.catch(err => {});
			// this.followShow = false;
		},
		// 取消关注
		handleCancelFollow(val) {
			cancelFollowing({ lawyer_id: val.lawyer_id })
				.then(res => {
					if (res.statusCode === 200) {
						uni.showToast({
							title: '已取消关注',
							icon: 'none'
						});
					} else if (res.statusCode === 401) {
						uni.navigateTo({
							url: '/pages/user/login'
						});
					}
				})
				.catch(err => {});
		},
		// 追问
		handleAsk(index) {
			this.askShow = index;
		},
		// 追问
		formSubmit() {},
		// 付费咨询
		handleConsult(obj) {}
	}
};
</script>

<style>
image,
swiper,
.img-view {
	width: 750upx;
	height: 500upx;
}
.page-section-title {
	margin-top: 50upx;
}
uni-image {
	width: 35px;
	height: 35px;
}
.uni-row uni-image {
	width: 90%;
	height: 90%;
}
</style>
