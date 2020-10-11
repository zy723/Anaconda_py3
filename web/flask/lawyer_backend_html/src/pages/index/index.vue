<template>
	<view>
		<view class="example-body">
			<view class="content">
				<uni-swiper-dot :info="info" :current="current" :mode="mode" :dots-styles="dotsStyles" field="content">
					<swiper class="swiper-box" @change="change">
						<swiper-item v-for="(item, index) in info" :key="index">
							<view :class="item.colorClass" class="swiper-item"><image :src="item.url" mode="aspectFill" /></view>
						</swiper-item>
					</swiper>
				</uni-swiper-dot>
			</view>
			<!-- 弹层 -->
			<view class="clear">
				<view class="column" @click="triggerCollapse">
					<view style="color: #333;font-size:30px;" class="navicon ask" />
					<view class="fontStyle">我要提问</view>
					<view class="fontColor999">在线提问 免费服务</view>
				</view>
				<view class="column" @click="handleAdvisory">
					<view style="color: #333;font-size: 30px;" class="navicon consultation" />
					<view class="fontStyle">我要咨询</view>
					<view class="fontColor999">图文沟通 快速咨询</view>
				</view>
			</view>
			<view>
				<uni-drawer :visible="showRigth" mode="right" class="uni-drawer-box">
					<span class="upicon"></span>
					<uni-list>
						<uni-list-item title="个人中心" @click="handleUser" />
						<uni-list-item :show-badge="true" title="消息通知" badge-text="12" />
					</uni-list>
				</uni-drawer>
			</view>
		</view>
		<view class="titleInfo example-title indexTit">
			最新法律提问
			<span class="title-line"></span>
		</view>
		<view class="example-box example-body">
			<view>
				<view class="uni-padding-wrap uni-common-mt">
					<view class="uni-list">
						<view class="uni-list-cell" hover-class="uni-list-cell-hover" v-for="(value, key) in listData" :key="key" @click="goDetail(value)">
							<view class="uni-media-list">
								<view class="uni-comment-face">
									<image src="../../../static/image/img1.png" class="iconTips" v-if="value.profile_photo === null"></image>
									<image :src="value.author_photo_url" v-else></image>
									<!-- <span class="vicon" v-if="value.is_certified"></span> -->
								</view>
								<view class="uni-media-list-body">
									<view class="uni-media-list-text-top">{{ value.title }}</view>
									<view class="uni-media-list-text-top">{{ value.author_name }}</view>
									<view class="uni-media-list-text-time">
										<text>{{ value.create_time }}{{ value.city }}</text>
									</view>
									<view class="uni-media-list-text-bottom">
										<text>
											<image src="../../static/image/icon1.png" class="iconTips"></image>
											{{ value.expertise }}
										</text>
										<text>{{ value.answer_count }}人回答</text>
									</view>
								</view>
							</view>
						</view>
					</view>
					<uni-load-more  :loadingType="loadingType" :contentText="contentText" ></uni-load-more>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
import uniDrawer from '@/components/uni-drawer/uni-drawer.vue';
import uniList from '@/components/uni-list/uni-list.vue';
import uniListItem from '@/components/uni-list-item/uni-list-item.vue';
import uniSwiperDot from '@/components/uni-swiper-dot/uni-swiper-dot.vue';
import uniLoadMore from '@/components/uni-load-more/uni-load-more.vue';
import { homeList } from '@/api/index.js';
var dateUtils = require('../../common/util.js').dateUtils;
var _this,
	page = 1,
	timer = null;
export default {
	name: 'IndexHeader',
	components: { uniDrawer, uniList, uniListItem, uniSwiperDot, uniLoadMore },
	data() {
		return {
			title: 'Hello',
			value: '',
			leftWords: '1',
			input: '2',
			rightIcon: '3',
			rightWords: '4',
			visible: false,
			showRigth: false,
			showLeft: false,
			current: 0,
			mode: 'dot',
			dotsStyles: {},
			pagination: {
				cur_page: 1,
				per_page_count: 10
			},
			listData: [],
			last_id: '',
			reload: false,
			status: 'more',
			loadingText: '加载中...',
			loadingType: 0,//定义加载方式 0---contentdown  1---contentrefresh 2---contentnomore
			contentText: {
				contentdown: '上拉加载更多',
				contentrefresh: '加载中',
				contentnomore: '没有最新提问了'
			},
			info: [
				{
					url: '../../static/image/banner1.png'
				},
				{
					url: '../../static/image/banner1.png'
				},
				{
					url: '../../static/image/banner1.png'
				}
			]
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
	/**
	 *  点击导航栏 buttons 时触发  右边按钮
	 */
	onNavigationBarButtonTap(e) {
		this.showRigth = !this.showRigth;
	},
	// 监听页面加载，为上个页面传递的数据，用于页面传参
	onLoad() {
		_this = this;
		this.getList();
	},
	//监听下拉刷新动作的执行方法，每次手动下拉刷新都会执行一次
	onPullDownRefresh() {
		console.log('onPullDownRefresh');
		// this.reload = true;
		// this.last_id = '';
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
		inputChange: function() {
			// this.$emit('change', this.value)
		},
		rightClick: function() {
			// this.$emit("rightClick")
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
		// 列表页跳转到详情页
		goDetail: function(e) {
			uni.navigateTo({
				url: '/pages/template/ask-details/ask-details?id=' + e.id
			});
		},
		// 获取默认列表信息
		getList() {
			page = 1;
			this.loadingType = 0;
			uni.showNavigationBarLoading();
			//请求接口
			homeList({
				cur_page:page,
				per_page_count:10
			})
				.then(res => {
					if (res.statusCode == 200) {
						page++; //得到数据之后page+1
						_this.listData = res.data;
						uni.hideNavigationBarLoading();
						uni.stopPullDownRefresh(); //得到数据后停止下拉刷新
					}
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
			//请求接口
			homeList({
				cur_page:page,
				per_page_count:10
			})
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
		setTime: function(items) {
			var newItems = [];
			items.forEach(e => {
				newItems.push({
					author_name: e.author_name,
					cover: e.cover,
					id: e.id,
					post_id: e.post_id,
					published_at: e.published_at,
					title: e.title
				});
			});
			return newItems;
		},
		triggerCollapse: function() {
			uni.navigateTo({
				url: '/pages/template/my-ask/ask'
			});
		},
		// 我要咨询
		handleAdvisory: function(e) {
			uni.navigateTo({
				url: '/pages/template/my-advisory/advisory-list'
			});
		},
		// 个人中心
		handleUser: function() {
			uni.navigateTo({
				url: '/pages/template/user/user'
			});
		}
	}
};
</script>

<style>
	
</style>
