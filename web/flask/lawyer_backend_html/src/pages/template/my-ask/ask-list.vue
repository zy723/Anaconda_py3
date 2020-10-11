<template>
	<view>
		<view class="example-box">
			<view>
				<view class="uni-padding-wrap uni-common-mt">
					<view class="">
						<view class="uni-list-cell" hover-class="uni-list-cell-hover">
							<view>
								<view class="uni-media-list-body example-body askList" v-for="(value,num) in baseData" :key='num'>
									<view class="uni-media-list-text-top">
									<router-link :to="{path:'/pages/template/my-ask/details?id='+value.id}">{{value.title}}</router-link></view>
									<view class="uni-media-list-text-bottom">
										<text class="fontColor999">{{value.time}}</text>
										<text @click="handleDel"><i class="iconfont iconTips fontColor333">&#xe61b;</i></text>
										</view>
									<!-- 相关图片暂时不做 -->
									<view class="uni-flex uni-row">
										<view class="flex-item" v-for="(item,index) in value.picList" :key='index'>
											<image :src="item.url"></image>
										</view>
									</view>
									<view class="uni-media-list-text-bottom">
										<text>
											<i class="iconfont iconTips">&#xe611;</i>
											<!-- <image src="../../static/image/icon1.png" class="iconTips"></image> -->
											{{value.expertise}}
										</text>
										<text>{{value.cont}}人回答</text>
									</view>
									<view class="uni-media-list-text-bottom solveBox">
										<text>
											问题是否解决？
										</text>
										<text>
											<button size="mini" type="default">已解决</button>
											<button size="mini" class="fontColorfff">未解决</button>
										</text>
									</view>
								</view>
								
							</view>
						</view>
					</view>
				</view>
			</view>
		</view>		
		<!-- 评论区 end -->
		<span class="askIcon"><router-link to="/pages/template/my-ask/ask"><i></i>提问</router-link></span>
	</view>
</template>

<script>

import { homeDetails,following,cancelFollowing } from '@/api/index.js';
export default {
	components: {},
	data() {
		return {
			parentId: null,
			baseData: [
				{
					id:1,
					title:'主顾3人以上拘禁4天，有两个轻伤，请问是什么罪？ 可以起诉么？',
					time:'1天前',
					picList:[
						{
							'url':'../../../static/image/pic1.jpg'
						},
						{
							'url':'../../../static/image/pic2.jpg'
						},
						{
							'url':'../../../static/image/pic3.jpg'
						}
					],
					expertise:'继承问题',
					cont:'7',
					issolve:true
				},
				{
					id:2,
					title:'主顾3人以上拘禁4天，有两个轻伤，请问是什么罪？ 可以起诉么？',
					time:'1天前',
					picList:[
						{
							'url':'../../../static/image/pic1.jpg'
						},
						{
							'url':'../../../static/image/pic2.jpg'
						},
						{
							'url':'../../../static/image/pic3.jpg'
						}
					],
					expertise:'继承问题',
					cont:'7',
					issolve:true
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
		// this.getDetails()
	},
	methods: {
		// 获取详情信息
		getDetails:function(){
			homeDetails({'id':this.parentId}).then(res => {
				if(res.statusCode===200){
					this.baseData=res.data
					// 重新定义标题
					uni.setNavigationBarTitle({
						title:this.baseData.author.name
					});
				}
			}).catch(err=>{
				
			});
		},
		// 我要提问
		triggerCollapse: function() {
			uni.navigateTo({
				url: '/pages/template/my-ask/ask'
			});
		},
		handleDel:function(){
			
			uni.showModal({
			    // title: '提示',
			    content: '确定删除您的提问？',
			    success: function (res) {
			        if (res.confirm) {
			            uni.navigateTo({
			            	url: '/pages/template/my-ask/delect'
			            });
			        } else if (res.cancel) {
			            console.log('用户点击取消');
			        }
			    },
				})

			
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
