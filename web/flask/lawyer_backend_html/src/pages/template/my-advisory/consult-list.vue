<template>
	<view>
		<view class="example-box">
			<view>
				<view class="uni-padding-wrap uni-common-mt">
					<view class="uni-media-list-body example-body askList">
						<view class="uni-comment-list uni-list-cell" hover-class="uni-list-cell-hover" v-for="(value, num) in baseData" :key="num" v-if="baseData.length>0">
							<view class="uni-comment-face">
								<image src="../../../static/image/img1.png" class="iconTips" v-if="value.profile_photo === ''"></image>
								<image :src="value.profile_photo" v-else></image>
								<span class="vicon" v-if="value.is_certified"></span>
							</view>
							<view class="uni-comment-body">
								<view class="uni-comment-top">
									<text>{{ value.real_name }} 律师</text>
									<view class="rInfo">
										<button type="primary" size="mini" class="butDefault" @click="handleEval(value)">评价</button>
										<button type="primary" size="mini" @click="handleConsult(value)">再次咨询</button>
									</view>
								</view>
								<view class="uni-media-list-text-time">
									<text>{{ value.practice_year }}</text>
								</view>
								<view  class="fontNumber">
									{{value.title}}
								</view>
								<view class="chear consultBox">
									<span class="btntips fontColor999">
										付费咨询 已完成
									</span>
									<!-- <span class="btntips tipTime">
										咨询中  还有30:00到时
									</span> -->
									<view class="rInfo fontColor999">{{value.time}}</view>
								</view>
							</view>
						</view>
						<view class="nullInfo" v-else>
							<view class="attIcon"><image src="../../../static/image/icon013.png"></image></view>
							暂无关注律师，快去<router-link to="/pages/template/my-advisory/advisory-list">找律师</router-link>吧！
						</view>
					</view>
				</view>
			</view>
		</view>
		<!-- 评论区 end -->
	</view>
</template>

<script>
import { homeDetails, following, cancelFollowing } from '@/api/index.js';
export default {
	components: {},
	data() {
		return {
			parentId: null,
			baseData: [
				{
					id: 1,
					real_name:'李兰',
					title: '主顾3人以上拘禁4天，有两个轻伤，请问是什么罪？ 可以起诉么？',
					practice_year: '1天前',
					profile_photo:'',
					expertise: '继承问题',
					cont: '7',
					issolve: true,
					time:'3天前'
				},
				{
					id: 2,
					real_name:'李兰',
					title: '主顾3人以上拘禁4天，有两个轻伤，请问是什么罪？ 可以起诉么？',
					practice_year: '1天前',
					profile_photo:'',
					expertise: '继承问题',
					cont: '7',
					issolve: true,
					time:'16天前'
				}
			]
		};
	},
	/**
	 *  点击导航栏 buttons 时触发  右边按钮
	 */

	// 监听页面加载，为上个页面传递的数据，用于页面传参
	onLoad(options) {
		// this.parentId = JSON.parse(options.id); // 字符串转对象
		this.getDetails()
	},
	methods: {
		// 获取详情信息
		getDetails: function() {
			homeDetails({ id: this.parentId })
				.then(res => {
					if (res.statusCode === 200) {
						this.baseData = res.data;
						// 重新定义标题
						uni.setNavigationBarTitle({
							title: this.baseData.author.name
						});
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
		handleDel: function() {
			uni.showModal({
				// title: '提示',
				content: '确定删除您的提问？',
				success: function(res) {
					if (res.confirm) {
						uni.navigateTo({
							url: '/pages/template/my-ask/delect'
						});
					} else if (res.cancel) {
						console.log('用户点击取消');
					}
				}
			});
		},
		// 个人中心
		handleUser: function() {
			uni.navigateTo({
				url: '/pages/template/user/user'
			});
		},
		// 评价
		handleEval:function(val){
			uni.navigateTo({
				url: '/pages/template/my-advisory/my-evaluate?id='+val.id
			});
		},
		// 再次咨询
		// 评价
		handleConsult:function(val){
			// uni.navigateTo({
			// 	url: '/pages/template/my-advisory/my-evaluate'
			// });
		}
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
<style scoped>
	page {
		background-color: #fff !important;
	}
</style>
