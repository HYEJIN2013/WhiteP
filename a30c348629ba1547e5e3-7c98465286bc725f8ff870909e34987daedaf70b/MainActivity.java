
public class MainActivity {
    
    public void pickImage() {
        ImagePicker.pickImage(this);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (resultCode == RESULT_OK && requestCode == ImagePicker.REQUEST_PICK) {
            ImagePicker.beginCrop(this, resultCode, data);
        } else if (requestCode == ImagePicker.REQUEST_CROP) {
            Bitmap bitmap = ImagePicker.getImageCropped(this, resultCode, data,
                    ImagePicker.ResizeType.FIXED_SIZE, AVATAR_SIZE);
            if (imagePickerListener != null) {
                imagePickerListener.onImagePicked(bitmap);
            }
            Log.d(this, "bitmap picked: " + bitmap);
        } else {
            super.onActivityResult(requestCode, resultCode, data);
        }
    }
}