<template>
	<view class="uploads">
		<!-- 图片上传 -->
		<view class="upload-image-view">
			<!-- 标题已经省略 -->
			<!-- <view class='title'>上传xxxx图片</view> -->
			<block v-for="(image, index) in imageList" :key="index">
				<view class="image-view">
					<image :src="image" :data-src="image" @tap="previewImage"></image>
					<view class="del-btn" :data-index="index" @tap="deleteImage"><view class="baicha"></view></view>
				</view>
			</block>
			<view class="add-view" v-if="imageList.length < imageLength" @tap="chooseImage">
				<!-- 相机 -->
				<!-- <view class="xiangji">
								<view class="tixing"></view>
								<view class='changfx'>
									<view class='yuan1'>
										<view class='yuan2'></view>
									</view>
								</view>
							</view> -->

				<!-- 十字架 -->
				<view class="cross">
					<view class="transverse-line"></view>
					<view class="vertical-line"></view>
				</view>
			</view>
			<view class="info">上传证书/证件，不超过{{ imageLength }}张。(非必填)</view>
		</view>
		<!-- 图片上传 -->
	</view>
	
</template>

<script>

export default {
	name: 'uni-card',
	props:['imageList','imageLength','sourceTypeIndex','sizeTypeIndex'],
	methods: {
		//选择图片
		chooseImage() {
			this.$emit('chooseImage');
		},
		//预览图片
		previewImage(e) {
			this.$emit('previewImage',e);
		},
		// 删除图片
		deleteImage(e) {
			this.$emit('deleteImage',e);
		}
	}
};
</script>

<style>
@import '../../static/style/upload-imgs.css';
page {
	display: flex;
	flex-wrap: wrap;
	justify-content: center;
	align-items: flex-start;
	background-color: #ffffff;
}

.body-view {
	width: 100%;
	display: flex;
	flex-wrap: wrap;
	justify-content: center;
	align-items: flex-start;
}

.info-table {
	width: 100%;
	display: flex;
	flex-wrap: wrap;
	justify-content: center;
	align-items: flex-start;
	background-color: #ffffff;
}

.info-table .info-table-row {
	height: 120upx;
	width: 92%;
	display: flex;
	flex-wrap: nowrap;
	align-items: center;
	justify-content: space-between;
	border-bottom: 1upx solid rgba(204, 204, 204, 1);
}

.info-table .info-table-row .table-row-left {
	height: 40upx;
	font-size: 28upx;
	font-weight: 400;
	color: rgba(28, 28, 28, 1);
	line-height: 40upx;
}

.info-table .info-table-row .table-row-right {
	display: flex;
	align-items: center;
	justify-content: center;
}

.info-table .info-table-row .table-row-right image {
	width: 13upx;
	height: 24upx;
}

.info-table .info-table-row .table-row-right input {
	width: 560upx;
	height: 40upx;
	font-size: 28upx;
	font-weight: 400;
	color: rgba(28, 28, 28, 1);
	line-height: 40upx;
}

.table-btn-view {
	position: fixed;
	bottom: 27upx;
	width: 100%;
	display: flex;
	align-items: center;
	justify-content: center;
}

.table-btn-view .save-btn {
	width: 92%;
	height: 90upx;
	background: rgba(0, 170, 255, 1);
	border-radius: 10upx;
	color: #ffffff;
}

.uploads {
	width: 92%;
}
</style>
