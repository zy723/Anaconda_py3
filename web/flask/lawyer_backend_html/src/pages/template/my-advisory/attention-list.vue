<template>
	<view>
		<view>
			<view v-if="listData.length > 0">
				<view class="example-list example-body" v-for="(value, key) in listData" :key="key">
					<view class="uni-padding-wrap">
						<view class="">
							<view class="uni-comment-list">
								<view class="uni-comment-face">
									<image src="../../../static/image/img1.png" class="iconTips" v-if="value.profile_photo === null"></image>
									<image :src="value.profile_photo" v-else></image>
									<span class="vicon" v-if="value.is_certified"></span>
								</view>
								<view class="uni-comment-body">
									<view class="uni-comment-top">
										<text>{{ value.real_name }}</text>
										<view class="rInfo">
											<button type="primary" size="mini" @click="handleFollow(value)" v-if="value.is_following">关注</button>
											<button type="primary" size="mini" class="butFollow" @click="handleCancelFollow(value)" v-else>已关注</button>
										</view>
									</view>
									<view class="uni-media-list-text-time">
										<text>{{ value.practice_year }}{{ value.lawyer_firm }}</text>
									</view>
									<view class="uni-comment-content" @click="goDetail(value)">
										<span v-for="obj in value.expertises">{{ obj }}，</span>
									</view>
									<view class="userInfo">
										评分：
										<span class="colTip gradeTip">{{ value.l_score }}</span>
										已为
										<span class="numTip"><span>236</span></span>
										人提供服务
									</view>
									<view class="chear">
										<span class="btntips btnFontCol">
											咨询费用
											<span class="infoTips">（免费）</span>
											<span class="colTip">({{ value.paid_for_once }}元/次)</span>
										</span>
									</view>
								</view>
							</view>
						</view>
					</view>
				</view>
				<uni-load-more :status="status" :content-text="contentText" />
			</view>
			<view class="nullInfo" v-else>
				<view class="attIcon"><image src="../../../static/image/icon010.png"></image></view>
				暂无关注律师，快去<router-link to="/pages/template/my-advisory/advisory-list">找律师</router-link>吧！
			</view>
		</view>
	</view>
</template>

<script>
import uniLoadMore from '@/components/uni-load-more/uni-load-more.vue';

import baseApi from '@/api/baseData/baseData.js';
import { lawyerList, following, cancelFollowing } from '@/api/index.js';
var dateUtils = require('../../../common/util.js').dateUtils;
var _self,
	page = 1,
	timer = null;
export default {
	name: 'IndexHeader',
	components: { uniLoadMore },
	data() {
		return {
			current: 0,
			mode: 'dot',
			pId: '110101',
			// gradeData: '全部',
			listData: [],
			status: 'more',
			// followShow: false,
			contentText: {
				contentdown: '上拉加载更多',
				contentrefresh: '加载中',
				contentnomore: '没有最新提问了'
			},
			reload: false,
			byID: '1'
		};
	},

	// 监听页面加载，为上个页面传递的数据，用于页面传参
	onLoad() {
		_self = this;
		this.getList();
	},
	// 监测数据变动
	watch: {
		$route() {
			this.getList();
		}
	},
	//监听下拉刷新动作的执行方法，每次手动下拉刷新都会执行一次
	onPullDownRefresh() {
		this.reload = true;
		this.getList();
	},
	// 页面上拉触底事件的处理
	onReachBottom() {
		// this.status = 'more';
		// this.getList();
		if (timer != null) {
			clearTimeout(timer);
		}
		timer = setTimeout(function() {
			_this.getmorenews();
		}, 1000);
	},
	methods: {
		change(e) {
			this.current = e.detail.current;
		},
		// 详情页面
		goDetail: function(e) {
			uni.navigateTo({
				url: '/pages/template/my-advisory/details?id=' + e.id
			});
		},
		// 获取默认列表信息
		getList() {
			var data = {
				by: this.byID, //需要的字段名
				p: this.pId
			};
			page = 1;
			this.loadingType = 0;
			uni.showNavigationBarLoading();
			lawyerList(
				data
				// {
				// 	cur_page:page,
				// 	per_page_count:10
				// }
			)
				.then(res => {
					page++; //得到数据之后page+1
					let list = res.data;
					// console.log(res.data)
					this.listData = list;
					this.reload = false;
					uni.hideNavigationBarLoading();
					uni.stopPullDownRefresh(); //得到数据后停止下拉刷新
				})
				.catch(err => {});
		},
		getmorenews() {
			if (_this.loadingType !== 0) {
				//loadingType!=0;直接返回
				return false;
			}
			_this.loadingType = 1;
			uni.showNavigationBarLoading(); //显示加载动画
			var data = {
				by: this.byID, //需要的字段名
				p: this.pId
			};
			//请求接口
			lawyerList(data)
				.then(res => {
					if (res.statusCode == 200) {
						if (res.data == null) {
							//没有数据
							_this.loadingType = 2;
							uni.hideNavigationBarLoading(); //关闭加载动画
							return;
						}

						page++; //每触底一次 page +1
						_this.listData = _this.listData.concat(res.data); //将数据拼接在一起
						_this.loadingType = 0; //将loadingType归0重置
						uni.hideNavigationBarLoading(); //关闭加载动画
						// console.log(_this.listData)
					}
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
					console.log(res);
					if (res.statusCode === 200) {
						uni.showToast({
							title: '已取消关注',
							icon: 'none'
						});
						this.getList();
					} else if (res.statusCode === 401) {
						uni.navigateTo({
							url: '/pages/user/login'
						});
					}
				})
				.catch(err => {});
		}
	}
};
</script>

<style scoped>
.example-body {
	padding-top: 5px;
	padding-bottom: 5px;
}
</style>
