<template>
	<view>
		<view class="example-body">
			<view class="uni-list">
				<view class="uni-list-cell">
					<view class="uni-list-cell-navigate uni-navigate-right uni-media-list " @click="handleHead">
						<view class="uni-media-list-logo">
							<image :src="baseData.user_photo_url"></image>
							<!-- <image :src="image"></image> -->
						</view>
						<view class="uni-media-list-body">
							<view>{{ baseData.user_name }}</view>
							<view class="fontColor999">修改头像</view>
						</view>
					</view>
				</view>
			</view>
		</view>
		<view class="example-body userList m15">
			<view class="uni-list">
				<view class="uni-list-cell">
					<view class="uni-triplex-row">
						<view class="uni-triplex-left">
							<text>
								<label>用户名</label>
								<text class="mRight">
									<span @click="handleTouch('name')" v-if="nameShow">{{ baseData.user_name }}</span>
									<input class="uni-input" v-else name="title" v-model="baseData.user_name" placeholder="请输入公司职位" />
								</text>
							</text>
						</view>
					</view>
				</view>
			</view>
			<view class="uni-list">
				<view class="uni-list-cell">
					<view class="uni-triplex-row">
						<view class="uni-triplex-left">
							<text>
								<label>性别</label>
								<text class="mRight">
									<span @click="handleTouch('gender')" v-if="genderShow">{{ baseData.gender }}</span>
									<input class="uni-input" name="title" v-else v-model="baseData.gender" placeholder="请输入公司职位" />
								</text>
							</text>
						</view>
					</view>
				</view>
			</view>
			<view class="uni-list">
				<view class="uni-list-cell">
					<view class="uni-triplex-row">
						<view class="uni-triplex-left">
							<text>
								<label>公司名</label>
								<text class="mRight">
									<span @click="handleTouch('company')" v-if="companyShow">
										<span v-if="baseData.company !== null">{{ baseData.company }}</span>
										<span v-else>暂无</span>
									</span>
									<input class="uni-input" name="title" v-else v-model="baseData.company" placeholder="请输入公司名字" />
								</text>
							</text>
						</view>
					</view>
				</view>
			</view>
			<view class="uni-list">
				<view class="uni-list-cell">
					<view class="uni-triplex-row">
						<view class="uni-triplex-left">
							<text>
								<label>公司职位</label>
								<text class="mRight">
									<span @click="handleTouch('position')" v-if="positionShow">
										<span v-if="baseData.position !== null">{{ baseData.position }}</span>
										<span v-else>暂无</span>
									</span>
									<input class="uni-input" name="title" v-else v-model="baseData.position" placeholder="请输入公司职位" />
								</text>
							</text>
						</view>
					</view>
				</view>
			</view>
			<view class="uni-list">
				<view class="uni-list-cell">
					<view class="uni-triplex-row">
						<view class="uni-triplex-left uni-media-list-body" @click="handleConsult">
							<text>
								<label>手机号码</label>
								<text class="mRight">
									<span @click="handleTouch('mobile')" v-if="mobileShow">{{ baseData.mobile }}</span>
									<input class="uni-input" name="title" v-else v-model="baseData.mobile" placeholder="请输入公司职位" />
								</text>
							</text>
						</view>
						<view class="uni-triplex-right "><i class="iconfont">&#xe615;</i></view>
					</view>
				</view>
			</view>
			<view class="table-btn-view bttomBox"><button class="save-btn" type="primary" form-type="submit" @click="handleRevamp">保存</button></view>
		</view>
	</view>
</template>

<script>
import uniNavBar from '@/components/uni-nav-bar/uni-nav-bar.vue';
import uniList from '@/components/uni-list/uni-list.vue';
import uniListItem from '@/components/uni-list-item/uni-list-item.vue';
import { userDetails, userRevamp, upPhoto } from '@/api/user.js';
var _this;
export default {
	components: { uniNavBar, uniList, uniListItem },
	data() {
		return {
			baseData: {},
			nameShow: true,
			genderShow: true,
			companyShow: true,
			positionShow: true,
			mobileShow: true,
			percent: 0,
			image: ''
		};
	},
	// 监听页面加载，为上个页面传递的数据，用于页面传参
	onLoad() {
		_this = this;

		// 重新定义标题
		uni.setNavigationBarTitle({
			title: '修改个人信息'
		});
		this.getDetails();
	},
	methods: {
		// 返回
		back() {
			uni.navigateBack({
				delta: 1
			});
		},
		// 获取个人详细信息
		getDetails() {
			userDetails()
				.then(res => {
					console.log(res)
					if (res.statusCode === 200) {
						this.baseData = res.data;
					}
					if (res.statusCode === 401) {
						uni.navigateTo({
							url: '/pages/user/login'
						});
					}
				})
				.catch(err => {});
		},
		// 点击修改基本信息
		handleTouch(obj) {
			if (obj === 'name') {
				this.nameShow = false;
			} else if (obj === 'gender') {
				this.genderShow = false;
			} else if (obj === 'company') {
				this.companyShow = false;
			} else if (obj === 'position') {
				this.positionShow = false;
			} else {
				this.mobileShow = false;
			}
		},
		// 保存个人信息
		handleRevamp() {
			userRevamp(this.baseData)
				.then(res => {
					if (res.statusCode === 200) {
						uni.showToast({
							icon: 'none',
							title: '修改成功'
						});
					}
				})
				.catch(err => {});
		},
		// 修改头像
		handleHead(e) {
			var token = uni.getStorageSync('access_token');
			uni.chooseImage({
				count: 1,
				sizeType: ['compressed'],
				success: function(res) {
					var imgFiles = res.tempFilePaths[0];
					upPhoto(imgFiles)
						.then(res => {
							if (res.statusCode === 200) {
								this.baseData.user_photo_url = JSON.parse(res.data).photo_url;
								uni.showToast({
									icon: 'none',
									title: '修改成功'
								});
							}
						})
						.catch(err => {});
				}
			});
		},
		// 详情
		handleConsult: function(e) {
			uni.navigateTo({
				url: '/pages/template/user/userPhoto'
			});
		}
	}
};
</script>

<style>
page {
	display: flex;
	flex-direction: column;
	box-sizing: border-box;
	background-color: #efeff4;
}
</style>
