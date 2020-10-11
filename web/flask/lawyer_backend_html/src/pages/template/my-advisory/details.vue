<template>
	<view>
		<!-- head -->
		<view class="headerInfo">
			<uni-nav-bar left-icon="arrowleft" title="律师主页" @click-left="back" class="homeList" :color="color" />
			<!-- 详细信息 -->
			<view class="userInfoBox">
				<view class="uni-padding-wrap">
					<view class="">
						<view class="uni-comment-list">
							<view class="uni-comment-face">
								<image src="../../../static/image/img1.png"></image>
								<image :src="baseData.profile_photo"></image>
								<span class="vicon"></span>
							</view>
							<view class="uni-comment-body">
								<view class="uni-comment-top">
									<text>{{ baseData.real_name }}</text>
									<view class="rInfo">
										<button type="primary" size="mini" @click="handleFollow(baseData)" v-if="baseData.is_following">关注</button>
										<button type="primary" size="mini" class="butFollow" @click="handleCancelFollow(baseData)" v-else>已关注</button>
									</view>
								</view>
								<view class="uni-comment-content">{{ baseData.practice_year }}{{ baseData.lawyer_firm }}</view>
								<!-- <view class="uni-comment-content">{{ baseData.content }}</view> -->
								<view class="userInfo">
									已为
									<span class="numTip">
										<span>{{ baseData.service_count }}</span>
									</span>
									人提供服务
								</view>
							</view>
						</view>
					</view>
				</view>
			</view>
			<!-- end -->
			<view class="userInfoTip" v-if="baseData.paid_for_once === 0 && baseData.paid_for_hour === 0">
				咨询费用：
				<span>免费</span>
			</view>
			<view class="costTips" v-else>
				<view class="costInfo">
					<view>按次咨询</view>
					<view>
						<span class="colTip">￥{{ baseData.paid_for_once }}</span>
						/次
					</view>
					<view>有效期24小时</view>
				</view>
				<view class="costInfo">
					<view>按月咨询</view>
					<view>
						<span class="colTip">￥{{ baseData.paid_for_hour }}</span>
						/月
					</view>
					<view>有效期30天</view>
				</view>
			</view>
		</view>
		<!-- end -->
		<view class="bottomPosition">
			<!-- 认证信息 -->
			<view class="example-infobox example-body">
				<view>
					<view class="uni-padding-wrap uni-common-mt">
						<view class="example-title ">认证信息</view>
						<view class="infoBox">
							<p>执业证号：{{ baseData.expert_ident }}</p>
							<p>执业机构：{{ baseData.lawyer_firm }}</p>
						</view>
					</view>
				</view>
			</view>
			<!-- end -->
			<!-- 用户评论 -->
			<view class="example-infobox example-body">
				<view>
					<view class="uni-padding-wrap uni-common-mt">
						<view class="example-title ">
							用户评论
							<span class="userInfo fontSize12">
								已有
								<span class="numTip">
									<span>{{ numData }}</span>
								</span>
								人评论
							</span>
							<span class="rInfo fontSize12">
								评分：
								<span class="numTip">
									<span class="colTip">{{ baseData.l_score }}</span>
									<i class="iconfont">&#xe615;</i>
								</span>
							</span>
						</view>
						<!-- <view class="example-title " v-else>
							用户评论
							<span class="rInfo fontSize12">
								已有
								<span class="numTip"><span>{{numData}}</span></span>
								人评论
								<i class="iconfont">&#xe615;</i>
							</span>
						</view> -->
						<view class="commentBox">
							<view>
								<p>{{ baseData.good_post_count }}</p>
								<p>好评</p>
							</view>
							<view>
								<p>{{ baseData.mid_post_count }}</p>
								<p>中评</p>
							</view>
							<view>
								<p>{{ baseData.bad_post_count }}</p>
								<p>差评</p>
							</view>
						</view>
					</view>
				</view>
			</view>
			<!-- end -->
			<!-- 专业领域 -->
			<view class="example-infobox example-body">
				<view>
					<view class="uni-padding-wrap uni-common-mt">
						<view class="example-title ">专业领域</view>
						<view class="infoBox">
							<p>
								<span v-for="(val, index) in baseData.expertises" :key="index">{{ val }}，</span>
							</p>
						</view>
					</view>
				</view>
			</view>
			<!-- end -->
			<!-- 详细介绍 -->
			<view class="example-infobox example-body">
				<view>
					<view class="uni-padding-wrap uni-common-mt">
						<view class="example-title ">详细介绍</view>
						<view class="infoBox">
							<p>{{ baseData.profile }}</p>
						</view>
					</view>
				</view>
			</view>
			<!-- end -->
		</view>

		<view class="bottomBox"><button type="primary" @click="handleConsult">在线咨询</button></view>
	</view>
</template>

<script>
import { lawyerDetails, following, cancelFollowing } from '@/api/index.js';
import uniNavBar from '@/components/uni-nav-bar/uni-nav-bar.vue';
export default {
	components: { uniNavBar },
	data() {
		return {
			height: '44px',
			payShow: false,
			advisortId: '',
			baseData: {},
			numData: '',
			color: '#fff'
		};
	},
	// 监听页面加载，为上个页面传递的数据，用于页面传参
	onLoad(options) {
		this.advisortId = options.id;
		this.getData(options.id);
	},
	created() {},
	methods: {
		// 返回首页
		back() {
			uni.navigateBack({
				delta: 1
			});
		},
		// 获取详情信息
		getData: function(id) {
			lawyerDetails(id)
				.then(ret => {
					this.baseData = ret.data;
					this.numData = Number(this.baseData.good_post_count) + Number(this.baseData.bad_post_count) + Number(this.baseData.mid_post_count);
				})
				.catch(err => {});
		},
		// 关注
		handleFollow(val) {
			following({ lawyer_id: val.id })
				.then(res => {
					// console.log(res);
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
		},
		// 取消关注
		handleCancelFollow(val) {
			cancelFollowing({ lawyer_id: val.id })
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
		// 咨询
		handleConsult: function(e) {
			let detail = {
				author_name: e.author_name,
				cover: e.cover,
				id: e.id,
				post_id: e.post_id,
				published_at: e.published_at,
				title: e.title
			};
			if (this.baseData.paid_for_once === 0 && this.baseData.paid_for_hour === 0) {
				uni.navigateTo({
					url: '/pages/template/my-advisory/chat?detailDate=' + encodeURIComponent(JSON.stringify(detail))
				});
			} else {
				uni.navigateTo({
					url: '/pages/template/my-advisory/pay?detailDate=' + encodeURIComponent(JSON.stringify(detail))
				});
			}
		}
	}
};
</script>

<style></style>
