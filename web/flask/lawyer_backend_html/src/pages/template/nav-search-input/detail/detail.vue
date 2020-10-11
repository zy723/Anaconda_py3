<template>
	<view class="wrapper">
		<view class="head">
			<uni-nav-bar v-if="listData.length > 0" left-icon="back" @click-left="back" title="搜索结果" class="searchreRsult"></uni-nav-bar>
			<uni-search-bar v-else radius="100" :isBack="true" ref="serchInfo" clearButton="always" @confirm="search" @cancel="cancel" @clearData="clearData"></uni-search-bar>
		</view>
		<!-- 搜索提示列表 -->
		<view class="history-box searchtips example-box example-body" v-if="searchVal">
			<view v-if="tipsData.length != 0" class="history-list-box">
				<view class="history-list-item" v-for="(item, index) in tipsData" :key="index" :data-value="item" @click="listTap"><rich-text :nodes="item"></rich-text></view>
			</view>
			<view v-if="tipsData.length == 0" class="no-data">没有搜索到相关内容</view>
		</view>
		<view class="history-box history example-box example-body" v-if="historyData.length != 0">
			<!-- 历史记录搜索 -->
			
			<view v-if="historyData.length>0">
				<view class="history-title">
					<text>搜索历史</text>
					<text class="uni-icon uni-icon-trash" @click="clearSearch"></text>
				</view>
				<view class="history-content">
					<view class="history-item" v-for="(item, index) in historyData" :key="index">{{ item }}</view>
				</view>
			</view>
			<view v-else class="no-data">{{historyList}}您还没有历史记录</view>
		</view>
		<!-- 搜索 -->
		<view class="example-box example-search" v-if="listData.length != 0">
			<!-- 律师信息 -->
			<view class="example-body">
				<view class="example-title titleNoBg">相关律师</view>
				<view class="userInfoBox">
					<view class="uni-padding-wrap">
						<view class="">
							<view class="uni-comment-list">
								<view class="uni-comment-face">
									<image :src="baseData.url"></image>
									<span class="vicon"></span>
								</view>
								<view class="uni-comment-body">
									<view class="uni-comment-top">
										<text>{{ baseData.name }}</text>
										<view class="rInfo"><button type="primary" size="mini" @click="handleConsult">咨询</button></view>
									</view>
									<view class="uni-comment-content">{{ baseData.content }}</view>
									<view class="userInfo">
										评分：
										<span class="colTip gradeTip">5.0</span>
										已为
										<span class="numTip"><span>236</span></span>
										人提供服务
									</view>
									<view class="chear">
										<span class="btntips btnFontCol">
											咨询费用
											<span class="infoTips">（免费）</span>
											<span class="colTip">(99元/次)</span>
										</span>
									</view>
								</view>
							</view>
						</view>
					</view>
				</view>
			</view>
			<view class="uni-list example-body" style="margin: 10px 0 0;">
				<view class="example-title ">相似问题</view>
				<view class="uni-list-cell" hover-class="uni-list-cell-hover" v-for="(value, key) in listData" :key="key" @click="goDetail(value)">
					<view class="uni-media-list">
						<!-- <image class="uni-media-list-logo" :src="value.cover"></image> -->
						<view class="uni-media-list-body">
							<view class="uni-media-list-text-top">
								<span v-if="value.title===null">暂无标题</span>
								<span v-else>{{ value.title }}</span>
							</view>
							<view class="uni-media-list-text-time">
								<text>{{ value.create_time }}{{ value.city }}</text>
							</view>
							<view class="uni-media-list-text-bottom">
								<text>
									<image src="../../../../static/image/icon1.png" class="iconTips"></image>
									{{ value.expertise }}
								</text>
								<text>{{ value.answer_count }}人回答</text>
							</view>
						</view>
					</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
import uniNavBar from '@/components/uni-nav-bar/uni-nav-bar.vue';
import uniSearchBar from '@/components/uni-search-bar/uni-search-bar.vue';
import util from '@/components/amap-wx/js/util.js';
import { tipList, searchList, historyList, clearHistory } from '@/api/index.js';

export default {
	components: {
		uniSearchBar,
		uniNavBar
	},
	data() {
		return {
			historyData: [],
			tipsData: [],
			// isHistory: true,
			listData: [],
			list: [],
			flng: true,
			timer: null,
			listShow: false,
			searchVal: '',
			baseData: {
				url: '/static/image/img1.png',
				name: '李琦律师',
				content: '从业8年  广东诺诚律师事务所'
			}
		};
	},
	// 监听页面加载，为上个页面传递的数据，用于页面传参
	onLoad() {
		// 本示例用的是高德 sdk ，请根据具体需求换成自己的服务器接口。
		this.amapPlugin = util.mapInit();
		// this.historyList = uni.getStorageSync('search:history');
		this.getHistoryData();
		// this.searchVal=this.$refs.serchInfo.searchVal
	},
	methods: {
		// 返回首页
		back() {
			uni.navigateBack({
				delta: 1
			});
		},
		// 鼠标触发获取提示列表
		search(e) {
			this.getInputtips(e);
		},
		// input(res) {
		// 	this.searchVal = res.value;
		// },
		// 搜索取消
		cancel(res) {
			// this.isHistory = false;
			this.listShow = false;
		},
		// 点击X清除列表数据
		clearData() {
			this.tipsData = [];
			this.listData = [];
		},
		/**
		 * 提示列表点击
		 */
		listTap(e) {
			var vaule = e.currentTarget.dataset.value;
			this.searchVal = vaule || this.searchVal;
			this.$refs.serchInfo.searchVal = vaule;
			this.getSearchData(this.searchVal);
		},
		// 获取查询列表数据
		getSearchData(vaule) {
			var data = {
				k: this.searchVal,
				cur_page: 1,
				per_page_count: 10
			};
			searchList(data)
				.then(res => {
					this.listShow = true;
					// this.isHistory = false;
					this.listData = res.data;
					if (this.listData.length > 0) {
						this.searchVal = '';
						this.historyData = [];
					}

					console.log(this.listData);
				})
				.catch(err => {});
		},
		// 历史列表数据
		getHistoryData(vaule) {
			historyList()
				.then(res => {
					if (res.statusCode == 200) {
						this.historyData = res.data.history_searching_list;
						console.log(this.historyData.length);
					}
				})
				.catch(err => {});
		},
		/**
		 * 清理历史搜索数据
		 */
		clearSearch() {
			clearHistory()
				.then(res => {
					this.historyData = [];
				})
				.catch(err => {});
		},
		// 获取提示列表数据
		getInputtips(e) {
			this.searchVal = e.detail.value;

			let _this = this;
			let text = e.detail.value;
			tipList({ k: this.searchVal })
				.then(res => {
					this.listShow = true;
					// this.isHistory = false;
					if (res.statusCode == 200) {
						this.tipsData = res.data;
					}
				})
				.catch(err => {});
		},
		onNavigationBarButtonTap(e) {
			uni.showModal({
				title: '提示',
				content: '点击确定，修改输入框的内容为abc',
				success: res => {
					if (res.confirm) {
						const currentWebview = this.$mp.page.$getAppWebview();
						currentWebview.setTitleNViewSearchInputText('abc');
					}
				}
			});
		},
		// 咨询
		handleConsult: function(e) {
			if (this.baseData.paid_for_once === 0 && this.baseData.paid_for_hour === 0) {
				uni.navigateTo({
					url: '/pages/template/my-advisory/chat'
				});
			} else {
				uni.navigateTo({
					url: '/pages/template/my-advisory/pay'
				});
			}
		}
	},
	// 返回首页
	back() {
		uni.navigateBack({
			delta: 1
		});
	}
};
</script>

<style>
.history-title {
	display: flex;
	justify-content: space-between;
	padding: 20upx 30upx;
	padding-bottom: 0;
	font-size: 34upx;
	color: #333;
}
.history-title .uni-icon {
	font-size: 40upx;
}
.history-content {
	display: flex;
	flex-wrap: wrap;
	padding: 15upx;
}
.history-item {
	padding: 4upx 35upx;
	border: 1px #f1f1f1 solid;
	background: #fff;
	border-radius: 50upx;
	margin: 12upx 10upx;
	color: #999;
}
.history-list-box {
	/* margin: 10upx 0; */
}
.history-list-item {
	padding: 30upx 0;
	margin-left: 30upx;
	border-bottom: 1px #eeeeee solid;
	font-size: 28upx;
}

.no-data {
	text-align: center;
	color: #999;
	margin: 100upx;
}
</style>
