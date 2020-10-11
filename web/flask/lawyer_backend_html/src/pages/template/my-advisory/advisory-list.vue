<template>
	<view>
		<view class="example-body">
			<view class="content">
				<uni-swiper-dot :info="bannerData" :current="current" :mode="mode" :dots-styles="dotsStyles" field="content">
					<swiper class="swiper-box" @change="change">
						<swiper-item v-for="(item, index) in bannerData" :key="index">
							<view class="swiper-item-hot backgrounds" :class="'backgrounds' + index">
								<view class="userName">{{ item.real_name }} 律师</view>
								<view class="userJob">
									<span>{{ item.lawyer_firm }}</span>
								</view>
								<view class="bannerList">
									<span v-for="(val, i) in item.expertises" :key="i">{{ val }}/</span>
								</view>
								<view class="userPhone">
									<i class="iconfont">&#xe61d;</i>
									{{ item.mobile }}
								</view>
								<!-- <image :src="'http://q10gxse55.bkt.clouddn.com/'+item.profile_photo" mode="aspectFill" /> -->
							</view>
						</swiper-item>
					</swiper>
				</uni-swiper-dot>
			</view>

			<view>
				<uni-drawer :visible="showRigth" mode="right" @close="closeDrawer('right')" class="uni-drawer-box">
					<span class="upicon"></span>
					<uni-list>
						<uni-list-item title="个人中心" @click="handleUser" />
						<uni-list-item :show-badge="true" title="消息通知" badge-text="12" />
					</uni-list>
				</uni-drawer>
			</view>
		</view>
		<view class="example-select example-body">
			<view class="uni-product-list">
				<view class="uni-product">
					<view class="image-view" @tap="popup_bottom()">
						地区
						<i class="iconfont">&#xe614;</i>
					</view>
					<linkAddress ref="linkAddress" :height="height" @confirmCallback="confirmCallback"></linkAddress>
				</view>
				<view class="uni-product">
					<view class="image-view" @tap="togglePopup()">
						专业领域
						<i class="iconfont">&#xe614;</i>
					</view>
					<uni-popup ref="popup" :height="height" @classCallback="classCallback" :bottomData="bottomData"></uni-popup>
				</view>
				<view class="uni-product">
					<view class="image-view" @tap="togglePopup('grade')">
						评分
						<i class="iconfont">&#xe614;</i>
					</view>
					<uni-popup ref="gradepopup" :height="height" @classCallback="classCallback('3')" :bottomData="gradeType"></uni-popup>
				</view>
			</view>
		</view>
		<view>
			<view v-if="listData.length > 0">
				<view class="example-list example-body" v-for="(value, key) in listData" :key="key">
					<view class="uni-padding-wrap">
						<view class="">
							<view class="uni-comment-list">
								<view class="uni-comment-face">
									<image src="../../../static/image/img1.png" class="iconTips" v-if="value.profile_photo === null"></image>
									<image :src="'http://q10gxse55.bkt.clouddn.com/' + value.profile_photo" v-else></image>
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
										<span class="numTip">
											<span>{{ value.service_count }}</span>
										</span>
										人提供服务
									</view>
									<view class="chear">
										<span class="btntips btnFontCol">
											咨询费用
											<span class="infoTips" v-if="value.paid_for_hour === 0 && value.paid_for_once === 0">（免费）</span>
											<span class="colTip" v-else-if="value.paid_for_once !== 0">({{ value.paid_for_once }}元/次)</span>
											<span class="colTip" v-else>({{ value.paid_for_hour }}元/小时)</span>
										</span>
										<!-- 前期不做 -->
										<!-- <view class="rInfo btntips">推广</view> -->
									</view>
								</view>
							</view>
						</view>
					</view>
				</view>
				<uni-load-more :status="status" :content-text="contentText" />
			</view>
			<view class="nullInfo" v-else>暂无数据</view>
		</view>
	</view>
</template>

<script>
import uniLoadMore from '@/components/uni-load-more/uni-load-more.vue';
import uniDrawer from '@/components/uni-drawer/uni-drawer.vue';
import uniList from '@/components/uni-list/uni-list.vue';
import uniListItem from '@/components/uni-list-item/uni-list-item.vue';
import uniSwiperDot from '@/components/uni-swiper-dot/uni-swiper-dot.vue';
import linkAddress from '@/components/address/address.vue';
import uniPopup from '@/components/uni-popup/uni-popup.vue';
import baseApi from '@/api/baseData/baseData.js';
import { lawyerList, hotlawyerList, following, cancelFollowing, getType } from '@/api/index.js';
import { token } from '@/api/login.js';
var dateUtils = require('../../../common/util.js').dateUtils;
var _self,
	page = 1,
	timer = null;
export default {
	name: 'IndexHeader',
	components: { uniDrawer, uniList, uniListItem, uniSwiperDot, uniLoadMore, linkAddress, uniPopup },
	data() {
		return {
			title: '',
			value: '',
			input: '2',
			visible: false,
			showRigth: false,
			showLeft: false,
			current: 0,
			mode: 'dot',
			dotsStyles: {},
			height: '100%',
			pId: '110101',
			territoryData: '公司专场',
			// gradeData: '全部',
			listData: [],
			status: 'more',
			// followShow: false,
			contentText: {
				contentdown: '上拉加载更多',
				contentrefresh: '加载中',
				contentnomore: '没有最新提问了'
			},
			last_id: '',
			reload: false,
			bottomData: [],
			gradeType: baseApi.gradeType,
			info: [
				{
					url: '../../../static/image/banner2.png'
				},
				{
					url: '../../../static/image/banner3.png'
				}
			],
			byID: '1'
		};
	},
	// 监听导航按钮事件
	onNavigationBarButtonTap(e) {
		this.showRigth = !this.showRigth;
	},
	// 监听页面加载，为上个页面传递的数据，用于页面传参
	onLoad() {
		_self = this;
		this.getList();
		this.getHotList();
		this.GetType();
	},
	// 监测数据变动
	watch: {
		$route() {
			this.getList();
		}
	},
	//监听下拉刷新动作的执行方法，每次手动下拉刷新都会执行一次
	onPullDownRefresh() {
		console.log('onPullDownRefresh');
		this.reload = true;
		this.getList();
	},
	// 页面上拉触底事件的处理
	onReachBottom() {
		this.status = 'more';
		this.getList();
	},
	methods: {
		// 弹层显示
		show(e) {
			if (e === 'left') {
				this.showLeft = true;
			} else {
				this.showRigth = true;
			}
		},
		// 弹层隐藏
		hide() {
			this.showLeft = false;
			this.showRigth = false;
		},
		// 头部个人中心
		closeDrawer(e) {
			if (e === 'left') {
				this.showLeft = false;
			} else {
				this.showRigth = false;
			}
		},

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
			lawyerList(data)
				.then(res => {
					let list = res.data;
					// console.log(res.data)
					this.listData = list;
					this.reload = false;
				})
				.catch(err => {});
		},
		getHotList() {
			hotlawyerList()
				.then(res => {
					this.bannerData = res.data.lawyer_list;
					for (var i = 0; i < this.bannerData.length; i++) {
						let phone = this.bannerData[i].mobile;
						this.bannerData[i].mobile = phone.replace(/^(.{3})(.*)(.{4})$/, '$1 - $2 - $3');
					}
				})
				.catch(err => {});
		},
		// 问题类型
		GetType() {
			getType()
				.then(res => {
					this.bottomData = res.data.data_list;
					this.classData.expertise_id = this.bottomData[0].expertise_id;
					this.classData.expertise_name = this.bottomData[0].expertise_name;
					console.log(res.data.data_list);
				})
				.catch(err => {});
		},
		//点击弹出弹窗
		popup_bottom: function() {
			this.height = '550rpx';
			//显示
			this.show_popup();
		},
		//显示弹窗
		show_popup: function() {
			this.$refs.linkAddress.show();
		},
		//回掉
		confirmCallback: function(byId) {
			this.byID = byId;
			let ads = this.$store.state.user_address;
			this.pId = String(ads.district.id);
			this.getList();
		},
		//回掉专业领域，评分
		classCallback: function(byId) {
			let ads = this.$store.state.classData;

			this.byID = byId;
			this.pId = ads.expertise_id;
			this.getList();
		},
		togglePopup: function(type) {
			this.height = '550rpx';
			if (type === 'grade') {
				this.$refs.gradepopup.show();
			} else {
				this.$refs.popup.show();
			}
		},
		// 个人中心
		handleUser: function() {
			uni.navigateTo({
				url: '/pages/template/user/user'
			});
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
