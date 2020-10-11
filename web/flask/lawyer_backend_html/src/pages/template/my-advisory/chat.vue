<template>
	<view>
		<view class="example-box example-body">
			<view class="uni-column">
				<view class="content" id="content" :style="{ height: style.contentViewHeight + 'px' }">
					<scroll-view id="scrollview" scroll-y="true" :style="{ height: style.contentViewHeight + 'px' }" :scroll-with-animation="true" :scroll-top="scrollTop">
						<message-show v-for="(message, index) in messages" :key="index" v-bind:message="message" :id="index"></message-show>
						<view id="bottom"></view>
					</scroll-view>
				</view>
				<view class="foot"><chat-input @send-message="getInputMessage"></chat-input></view>
			</view>
		</view>
		<!-- 弹层 -->
		<uni-popups ref="popups" :type="type"  @change="change" class="popupBox">
			<div class="poputComBox">
				<p>请给我一个评价吧</p>
				<view class="comBtn">去评价</view>
			</div>
			
		</uni-popups>
		<uni-drawer :visible="showRigth" mode="right" @close="closeDrawer('right')">
			<span class="upicon"></span>
			<uni-list>
				<uni-list-item title="个人中心" />
				<uni-list-item :show-badge="true" title="消息通知" badge-text="12" />
			</uni-list>
		</uni-drawer>
	</view>
</template>

<script>
import uniDrawer from '@/components/uni-drawer/uni-drawer.vue';
import uniList from '@/components/uni-list/uni-list.vue';
import uniListItem from '@/components/uni-list-item/uni-list-item.vue';
import chatInput from '@/components/uni-chat/chatinput.vue';
import messageShow from '@/components/uni-chat/messageshow.vue';
import uniPopups from '@/components/uni-popup/uni-popups.vue';
export default {
	components: { uniDrawer, uniList, uniListItem, chatInput, messageShow ,uniPopups},
	data() {
		return {
			showSwiper: false,
			visible: false,
			showRigth: false,
			showLeft: false,
			followShow: true,
			style: {
				pageHeight: 0,
				contentViewHeight: 0,
				footViewHeight: 90,
				mitemHeight: 0
			},
			type:'',
			scrollTop: 0,
			messages: [
				{
					user: 'home',
					type: 'head', //input,content
					content: '你好!'
				}
			]
		};
	},
	/**
	 * 当 searchInput 配置 disabled 为 true 时触发
	 */
	onNavigationBarSearchInputClicked(e) {
		console.log('事件执行了');
		uni.navigateTo({
			url: '/pages/template/nav-search-input/detail/detail'
		});
	},
	/**
	 *  点击导航栏 buttons 时触发
	 */
	onNavigationBarButtonTap(e) {
		this.showRigth = !this.showRigth;
	},
	onLoad() {
		// 重新定义标题
		uni.setNavigationBarTitle({
			title: '与张律师的对话'
		});
		
		
	},
	mounted() {
		console.log(this.$refs.popups)
		this.type = 'center'
		this.$refs.popups.open()
	},
	created: function() {
		
		// const res = uni.getSystemInfoSync();
		// this.style.pageHeight = res.windowHeight;
		// this.style.contentViewHeight = res.windowHeight - (uni.getSystemInfoSync().screenWidth / 750) * 100; //像素
	},
	methods: {
		show(e) {
			if (e === 'left') {
				this.showLeft = true;
			} else {
				this.showRigth = true;
			}
		},
		hide() {
			this.showLeft = false;
			this.showRigth = false;
		},
		closeDrawer(e) {
			if (e === 'left') {
				this.showLeft = false;
			} else {
				this.showRigth = false;
			}
		},
		change: function(e) {
			console.log(e.show);
		},
		// 关注
		handleFollow() {
			this.followShow = false;
		},
		getInputMessage: function(message) {
			//获取子组件的输入数据
			// console.log(message);
			this.addMessage('customer', message.content, false);
			this.toRobot(message.content);
		},
		addMessage: function(user, content, hasSub, subcontent) {
			var that = this;
			that.messages.push({
				user: user,
				content: content,
				hasSub: hasSub,
				subcontent: subcontent
			});
		},
		scrollToBottom: function() {
			var that = this;
			var query = uni.createSelectorQuery();
			query.selectAll('.m-item').boundingClientRect();
			query.select('#scrollview').boundingClientRect();

			query.exec(function(res) {
				that.style.mitemHeight = 0;
				res[0].forEach(function(rect) {
					// console.info(rect.height);
					that.style.mitemHeight = that.style.mitemHeight + rect.height + 20;
				});

				if (that.style.mitemHeight > that.style.contentViewHeight) {
					that.scrollTop = that.style.mitemHeight - that.style.contentViewHeight;
				}
			});
		},
		toRobot: function(info) {
			// this.addMessage('home', info, false);
			var apiUrl = 'http://www.tuling123.com/openapi/api';
			uni.request({
				url: apiUrl,
				data: {
					key: 'acfbca724ea1b5db96d2eef88ce677dc',
					info: info,
					userid: 'uni-test'
				},
				success: res => {
					this.addMessage('home', res.data.text, false);
					this.scrollToBottom();
					console.log('request success:' + res.data.text);
				},
				fail: err => {
					console.log('request fail', err);
					uni.showModal({
						content: err.errMsg,
						showCancel: false
					});
				}
			});
		}
	}
};
</script>

<style scoped>
/* 设置当前页的背景颜色 */
page {
	background-color: #fff !important;
}
.uni-column {
	display: flex;
	flex-direction: column;
}
.content {
	display: flex;
	flex: 1;
	margin-bottom: 100px;
}
.foot {
	position: fixed;
	width: 100%;
	height: 60px;
	min-height: 60px;
	left: 0px;
	bottom: 0px;
	overflow: hidden;
}
</style>
