<template>
	<view class="tabs">
		<scroll-view id="tab-bar" class="scroll-h" :scroll-x="true" :show-scrollbar="false" :scroll-into-view="scrollInto">
			<view v-for="(tab, index) in tabBars" :key="tab.id" class="uni-tab-item" :id="tab.id" :data-current="index" @click="ontabtap">
				<text class="uni-tab-item-title" :class="tabIndex == index ? 'uni-tab-item-title-active' : ''">{{ tab.name }}<span class="lineInfo"></span></text>
			</view>
		</scroll-view>
		<view class="line-h"></view>
		<swiper :current="tabIndex" class="swiper-box" style="flex: 1;" :duration="300" @change="ontabchange">
			<swiper-item class="swiper-item" v-for="(tab, index1) in newsList" :key="index1">
				<scroll-view class="scroll-v list" enableBackToTop="true" scroll-y @scrolltolower="loadMore(index1)">
					<view v-for="(value, index2) in tab.data" :key="value.id">
						<view class="uni-media-list">
							<view class="uni-comment-face">
								<image src="../../../static/image/img1.png" class="iconTips" v-if="value.profile_photo === ''"></image>
								<image :src="value.profile_photo" v-else></image>
								<span class="vicon" v-if="value.is_certified"></span>
							</view>
							<view class="uni-comment-body">
								<view class="uni-comment-top">
									<text>{{ value.real_name }} 律师</text>
									<view class="rInfo">
										<span class="colBlue" v-if="value.grade!==undefined">{{value.grade}}</span>
										<button type="primary" size="mini" @click="handleEval(value)" v-else>评价</button>
										
										</view>
								</view>
								<view class="uni-media-list-text-time"><text>从业律师10年</text></view>
								<view class="fontCol666 fontSize12">{{ value.practice_year }}</view>
							</view>
						</view>
					</view>
					<view class="loading-more" v-if="tab.isLoading || tab.data.length > 4">
						<text class="loading-more-text">{{ tab.loadingText }}</text>
					</view>
				</scroll-view>
			</swiper-item>
		</swiper>
	</view>
</template>
<script>
import mediaItem from '@/components/uni-tabbar/news-item.vue';
import { homeList } from '@/api/index.js';
var _this,
	page = 1,
	timer = null;
// 缓存每页最多
const MAX_CACHE_DATA = 100;
// 缓存页签数量
const MAX_CACHE_PAGE = 3;

const newsData = {};

export default {
	components: {
		mediaItem
	},
	data() {
		return {
			newsList: [],
			cacheTab: [],
			tabIndex: 0,
			tabBars: [
				{
					name: '待评价'
				},
				{
					name: '已评价'
				}
			],
			scrollInto: '',
			showTips: false,
			navigateFlag: false,
			pulling: false,
			baseData: [
				{
					id: 1,
					real_name: '李兰',
					title: '主顾3人以上拘禁4天，有两个轻伤，请问是什么罪？ 可以起诉么？',
					practice_year: '1天前',
					profile_photo: '',
					expertise: '继承问题',
					cont: '7',
					issolve: true,
					time: '3天前'
				},
				{
					id: 2,
					real_name: '李兰',
					title: '主顾3人以上拘禁4天，有两个轻伤，请问是什么罪？ 可以起诉么？',
					practice_year: '1天前',
					profile_photo: '',
					expertise: '继承问题',
					cont: '7',
					issolve: true,
					time: '16天前'
				}
			],
			evlaData:[
				{
					id: 1,
					real_name: '李兰',
					title: '主顾3人以上拘禁4天，有两个轻伤，请问是什么罪？ 可以起诉么？',
					practice_year: '1天前',
					profile_photo: '',
					expertise: '继承问题',
					grade: '7分',
					issolve: true,
					time: '16天前'
				}
			]
		};
	},
	onLoad() {
		setTimeout(() => {
			this.tabBars.forEach(tabBar => {
				this.newsList.push({
					data: [],
					isLoading: false,
					refreshText: '',
					loadingText: '加载更多...'
				});
			});
			this.getList(0);
		}, 350);
	},
	methods: {
		getList(index) {
			console.log(index)
			let activeTab = this.newsList[index];
			let list = [];
			// for (let i = 1; i <= 10; i++) {
			//     let item = Object.assign({}, newsData['data' + Math.floor(Math.random() * 5)]);
			//     item.id = this.newGuid();
			//     list.push(item);
			// }
			//请求接口
			page = 1;
			// homeList({
			// 	cur_page:page,
			// 	per_page_count:10
			// })
			// 	.then(res => {
			// 		if (res.statusCode == 200) {
			// 			let list = res.data;
			// 			activeTab.data = activeTab.data.concat(list);
			// 		}
			// 	})
			// 	.catch(err => {});
			if(index===0){
				activeTab.data = this.baseData;
				console.log(this.baseData[0].grade)
			}else{
				activeTab.data = this.evlaData;
			}
			
		},
		goDetail(e) {
			if (this.navigateFlag) {
				return;
			}
			this.navigateFlag = true;
			uni.navigateTo({
				url: './detail/detail?title=' + e.title
			});
			setTimeout(() => {
				this.navigateFlag = false;
			}, 200);
		},
		close(index1, index2) {
			uni.showModal({
				content: '是否删除本条信息？',
				success: res => {
					if (res.confirm) {
						this.newsList[index1].data.splice(index2, 1);
					}
				}
			});
		},
		loadMore(e) {
			setTimeout(() => {
				this.getList(this.tabIndex);
			}, 500);
		},
		ontabtap(e) {
			let index = e.target.dataset.current || e.currentTarget.dataset.current;
			this.switchTab(index);
		},
		ontabchange(e) {
			let index = e.target.current || e.detail.current;
			this.switchTab(index);
		},
		switchTab(index) {
			if (this.newsList[index].data.length === 0) {
				this.getList(index);
			}

			if (this.tabIndex === index) {
				return;
			}

			// 缓存 tabId
			if (this.newsList[this.tabIndex].data.length > MAX_CACHE_DATA) {
				let isExist = this.cacheTab.indexOf(this.tabIndex);
				if (isExist < 0) {
					this.cacheTab.push(this.tabIndex);
					//console.log("cache index:: " + this.tabIndex);
				}
			}

			this.tabIndex = index;
			this.scrollInto = this.tabBars[index].id;

			// 释放 tabId
			if (this.cacheTab.length > MAX_CACHE_PAGE) {
				let cacheIndex = this.cacheTab[0];
				this.clearTabData(cacheIndex);
				this.cacheTab.splice(0, 1);
				//console.log("remove cache index:: " + cacheIndex);
			}
		},
		clearTabData(e) {
			this.newsList[e].data.length = 0;
			this.newsList[e].loadingText = '加载更多...';
		},
		refreshData() {},
		onrefresh(e) {
			var tab = this.newsList[this.tabIndex];
			if (!tab.refreshFlag) {
				return;
			}
			tab.refreshing = true;
			tab.refreshText = '正在刷新...';

			setTimeout(() => {
				this.refreshData();
				this.pulling = true;
				tab.refreshing = false;
				tab.refreshFlag = false;
				tab.refreshText = '已刷新';
				setTimeout(() => {
					// TODO fix ios和Android 动画时间相反问题
					this.pulling = false;
				}, 500);
			}, 2000);
		},
		onpullingdown(e) {
			var tab = this.newsList[this.tabIndex];
			if (tab.refreshing || this.pulling) {
				return;
			}
			if (Math.abs(e.pullingDistance) > Math.abs(e.viewHeight)) {
				tab.refreshFlag = true;
				tab.refreshText = '释放立即刷新';
			} else {
				tab.refreshFlag = false;
				tab.refreshText = '下拉可以刷新';
			}
		},
		handleEval(){
			uni.navigateTo({
				url: '/pages/template/my-advisory/my-evaluate'
			});
		},
		newGuid() {
			let s4 = function() {
				return ((65536 * (1 + Math.random())) | 0).toString(16).substring(1);
			};
			return (s4() + s4() + '-' + s4() + '-4' + s4().substr(0, 3) + '-' + s4() + '-' + s4() + s4() + s4()).toUpperCase();
		}
	}
};
</script>

<style>
/* #ifndef APP-PLUS */
page {
	width: 100%;
	min-height: 100%;
	display: flex;
}

/* #endif */

.tabs {
	flex: 1;
	flex-direction: column;
	overflow: hidden;
	background-color: #ffffff;
	/* #ifdef MP-ALIPAY || MP-BAIDU */
	height: 100vh;
	/* #endif */
}

.scroll-h {
	width: 750upx;
	height: 80upx;
	flex-direction: row;
	/* #ifndef APP-PLUS */
	white-space: nowrap;
	/* #endif */
	/* flex-wrap: nowrap; */
	/* border-color: #cccccc;
		border-bottom-style: solid;
		border-bottom-width: 1px; */
}

.line-h {
	height: 1upx;
	background-color: #f1f1f1;
}

.uni-tab-item {
	/* #ifndef APP-PLUS */
	display: inline-block;
	/* #endif */
	flex-wrap: nowrap;
	padding-left: 34upx;
	padding-right: 34upx;
}

.uni-tab-item-title {
	color: #555;
	font-size: 30upx;
	height: 80upx;
	line-height: 80upx;
	flex-wrap: nowrap;
	/* #ifndef APP-PLUS */
	white-space: nowrap;
	/* #endif */
}

.uni-tab-item-title-active {
	color: #007aff;
	position:relative;
}
.uni-tab-item-title-active span.lineInfo{
	border-bottom: 2px solid #007aff;
	width:30px;
	    display: inline-block;
	    position: absolute;
	    bottom: -12px;
	    left: 50%;
	    margin-left: -15px;
}
.swiper-box {
	flex: 1;
}

.swiper-item {
	flex: 1;
	flex-direction: row;
}

.scroll-v {
	flex: 1;
	/* #ifndef MP-ALIPAY */
	flex-direction: column;
	/* #endif */
	width: 750upx;
}

.update-tips {
	position: absolute;
	left: 0;
	top: 41px;
	right: 0;
	padding-top: 5px;
	padding-bottom: 5px;
	background-color: #fddd9b;
	align-items: center;
	justify-content: center;
	text-align: center;
}

.update-tips-text {
	font-size: 14px;
	color: #ffffff;
}

.refresh {
	width: 750upx;
	height: 64px;
	justify-content: center;
}

.refresh-view {
	flex-direction: row;
	flex-wrap: nowrap;
	align-items: center;
	justify-content: center;
}

.refresh-icon {
	width: 30px;
	height: 30px;
	transition-duration: 0.5s;
	transition-property: transform;
	transform: rotate(0deg);
	transform-origin: 15px 15px;
}

.refresh-icon-active {
	transform: rotate(180deg);
}

.loading-icon {
	width: 20px;
	height: 20px;
	margin-right: 5px;
	color: #999999;
}

.loading-text {
	margin-left: 2px;
	font-size: 16px;
	color: #999999;
}

.loading-more {
	align-items: center;
	justify-content: center;
	padding-top: 10px;
	padding-bottom: 10px;
	text-align: center;
}

.loading-more-text {
	font-size: 28upx;
	color: #999;
}
</style>
