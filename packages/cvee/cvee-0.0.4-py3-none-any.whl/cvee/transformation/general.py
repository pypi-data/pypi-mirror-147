import numpy as np
import torch

from cvee.utils.misc import is_array_or_tensor


def transform(pts, tf_mat):
    """Apply a transformation matrix on a set of 3D points. Note that this function is not differentiable.

    Args:
        pts (np.ndarray, torch.Tensor): 3D points, could be Nx3 or BxNx3(tensor only).
        tf_mat (np.ndarray, torch.Tensor): Transformation matrix, could be 4x4 or Bx4x4(tensor only).

        The types of tf_mat and pts should be consistent.

    Returns:
        Transformed pts. Return torch.Tensor if matrix and points are torch.Tensor, else np.ndarray.
    """
    if (not is_array_or_tensor(tf_mat)) or (not is_array_or_tensor(pts)):
        raise TypeError(f"tf_mat and pts should be np.ndarray or torch.Tensor, but got {type(tf_mat)} and {type(pts)}")
    if type(tf_mat) != type(pts):
        raise TypeError(f"The types of tf_mat and pts should be consistent, but got {type(tf_mat)} and {type(pts)}")

    return_tensor = isinstance(tf_mat, torch.Tensor) or isinstance(pts, torch.Tensor)

    if not return_tensor:  # return np.ndarray, tf_mat and pts are both np.ndarray
        if tf_mat.ndim != 2 or tf_mat.shape[0] != 4 or tf_mat.shape[1] != 4:
            raise RuntimeError(f"The size of tf_mat should be 4x4, but got {tf_mat.shape}")
        if pts.ndim != 2 or pts.shape[1] != 3:
            raise RuntimeError(f"The size of pts should be Nx3, but got {pts.shape}")

        pts = pts.copy()
        new_pts = np.concatenate([pts, np.ones([pts.shape[0], 1])], axis=1)
        new_pts = np.dot(tf_mat, new_pts.T).T
        new_pts = new_pts[:, :3].copy()
    else:  # return torch.tensor, tf_mat and pts are both torch.tensor
        if tf_mat.ndim == 2 and pts.ndim == 2:
            if tf_mat.shape[0] != 4 or tf_mat.shape[1] != 4:
                raise RuntimeError(f"The size of tf_mat should be 4x4, but got {tf_mat.shape}")
            if pts.shape[1] != 3:
                raise RuntimeError(f"The size of pts should be Nx3 or BxNx3, but got {pts.shape}")

            pts = pts.clone()
            new_pts = torch.cat([pts, torch.ones(pts.shape[0], 1).to(pts.device)], dim=1)
            new_pts = torch.transpose(torch.mm(tf_mat, torch.transpose(new_pts, 0, 1)), 0, 1)
            new_pts = new_pts[:, :3].clone()
        elif tf_mat.ndim == 3 and pts.ndim == 3:
            if tf_mat.shape[1] != 4 or tf_mat.shape[2] != 4:
                raise RuntimeError(f"The size of tf_mat should be 4x4, but got {tf_mat.shape}")
            if pts.shape[2] != 3:
                raise RuntimeError(f"The size of pts should be Nx3 or BxNx3, but got {pts.shape}")

            pts = pts.clone()
            padding = (torch.ones(pts.shape[0], pts.shape[1], 1).to(pts.device),)
            new_pts = torch.cat([pts, padding], dim=2)
            new_pts = torch.transpose(torch.bmm(tf_mat, torch.transpose(new_pts, 1, 2)), 1, 2)
            new_pts = new_pts[:, :, :3].clone()
        else:
            raise RuntimeError(f"Incorrect size of tf_mat or pts, tf_mat: {tf_mat.shape}, pts: {pts.shape}")

    return new_pts


# TODO: write test cases
def project(pts, intr_mat):
    """Project 3D points in the camera space to the image plane. Note that this function is not differentiable.

    Args:
        pts (np.ndarray, torch.Tensor): 3D points, could be Nx3 or BxNx3(tensor only).
        intr_mat (np.ndarray, torch.Tensor): Intrinsic matrix, could be 3x3 or Bx3x3(tensor only).

        The types of pts and intr_mat should be consistent.

    Returns:
        pixels, the order is uv other than xy.
        depth, depth in the camera space.
    """
    if (not is_array_or_tensor(intr_mat)) or (not is_array_or_tensor(pts)):
        raise TypeError(
            f"pts and intr_mat should be np.ndarray or torch.Tensor, but got {type(pts)} and {type(intr_mat)}"
        )
    if type(intr_mat) != type(pts):
        raise TypeError(f"The types of pts and intr_mat should be consistent, but got {type(pts)} and {type(intr_mat)}")

    return_tensor = isinstance(intr_mat, torch.Tensor) or isinstance(pts, torch.Tensor)

    if not return_tensor:  # return np.ndarray, tf_mat and pts are both np.ndarray
        if intr_mat.ndim != 2 or intr_mat.shape[0] != 3 or intr_mat.shape[1] != 3:
            raise RuntimeError(f"The size of intr_mat should be 3x3, but got {intr_mat.shape}")
        if pts.ndim != 2 or pts.shape[1] != 3:
            raise RuntimeError(f"The size of pts should be Nx3, but got {pts.shape}")

        pts = pts.copy()
        pts = pts / pts[:, 2:3]
        new_pts = np.dot(intr_mat, pts.T).T
        return new_pts[:, :2].copy()
    else:  # return torch.tensor, tf_mat and pts are both torch.tensor
        if intr_mat.ndim == 2 and pts.ndim == 2:
            if intr_mat.shape[0] != 3 or intr_mat.shape[1] != 3:
                raise RuntimeError(f"The size of tf_mat should be 3x3, but got {intr_mat.shape}")
            if pts.shape[1] != 3:
                raise RuntimeError(f"The size of pts should be Nx3 or BxNx3, but got {pts.shape}")

            pts = pts.clone()
            pts = pts / pts[:, 2:3]
            new_pts = torch.transpose(torch.mm(intr_mat, torch.transpose(pts, 0, 1)), 0, 1)
            return new_pts[:, :2].clone()
        elif intr_mat.ndim == 3 and pts.ndim == 3:
            if intr_mat.shape[1] != 3 or intr_mat.shape[2] != 3:
                raise RuntimeError(f"The size of intr_mat should be 3x3, but got {intr_mat.shape}")
            if pts.shape[2] != 3:
                raise RuntimeError(f"The size of pts should be Nx3 or BxNx3, but got {pts.shape}")

            pts = pts.clone()
            pts = pts / pts[..., 2:3]
            new_pts = torch.transpose(torch.bmm(intr_mat, torch.transpose(pts, 1, 2)), 1, 2)
            return new_pts[..., :2].clone()
        else:
            raise RuntimeError(f"Incorrect size of intr_mat or pts: {intr_mat.shape}, {pts.shape}")


# TODO: implement this
def unproject():
    raise NotImplementedError()


# TODO: write test cases
def rot_tl_to_tf_mat(rot_mat, tl):
    """Build transformation matrix with rotation matrix and translation vector.

    Args:
        rot_mat (np.ndarray, torch.Tensor): rotation matrix, could be 3x3 or Bx3x3(tensor only).
        tl (np.ndarray, torch.Tensor): translation vector, could be 3 or Bx3(tensor only).

        The types of rot_mat and tl should be consistent.

    Returns:
        tf_mat, transformation matrix. Return torch.Tensor if rot_mat and tl are torch.Tensor, else np.ndarray.
    """
    if (not is_array_or_tensor(rot_mat)) or (not is_array_or_tensor(tl)):
        raise TypeError(f"rot_mat and tl should be np.ndarray or torch.Tensor, but got {type(rot_mat)} and {type(tl)}")
    if type(rot_mat) != type(tl):
        raise TypeError(f"The types of rot_mat and tl should be consistent, but got {type(rot_mat)} and {type(tl)}")

    return_tensor = isinstance(rot_mat, torch.Tensor) or isinstance(tl, torch.Tensor)

    if not return_tensor:  # return np.ndarray, rot_mat and tl are both np.ndarray
        if rot_mat.ndim != 2 or rot_mat.shape[0] != 3 or rot_mat.shape[1] != 3:
            raise RuntimeError(f"The size of rot_mat should be 3x3, but got {rot_mat.shape}")
        if tl.ndim != 1 or tl.shape[0] != 3:
            raise RuntimeError(f"The size of tl should be 3, but got {tl.shape}")

        tf_mat = np.eye(4)
        tf_mat[:3, :3] = rot_mat
        tf_mat[:3, 3] = tl
        return tf_mat.copy()
    else:  # return torch.tensor, rot_mat and tl are both torch.tensor
        if rot_mat.ndim == 2 and tl.ndim == 1:
            if rot_mat.shape[0] != 3 or rot_mat.shape[1] != 3:
                raise RuntimeError(f"The size of rot_mat should be 3x3, but got {rot_mat.shape}")
            if tl.shape[0] != 3:
                raise RuntimeError(f"The size of tl should be 3, but got {tl.shape}")

            tf_mat = torch.eye(4)
            tf_mat[:, :3, :3] = rot_mat
            tf_mat[:, :3, 3] = tl
            return tf_mat.clone()
        elif rot_mat.ndim == 3 and tl.ndim == 2:
            if rot_mat.shape[0] != tl.shape[0]:
                raise RuntimeError(f"Different batch size: {rot_mat.shape}, {tl.shape}")
            if rot_mat.shape[1] != 3 or rot_mat.shape[2] != 3:
                raise RuntimeError(f"The size of rot_mat should be Bx3x3, but got {rot_mat.shape}")
            if tl.shape[1] != 3:
                raise RuntimeError(f"The size of tl should be Bx3, but got {tl.shape}")

            batch_size = rot_mat.shape[0]
            tf_mat = torch.eye(4).unsqueeze(0)
            tf_mat = tf_mat.repeat(batch_size, 1, 1)
            tf_mat[:, :3, :3] = rot_mat
            tf_mat[:, :3, 3] = tl
            return tf_mat.clone()
        else:
            raise RuntimeError(f"Incorrect size of rot_mat or tl: {rot_mat.shape}, {tl.shape}")


# TODO: write test cases
def cart_to_homo(pts_3d):
    """Convert Cartesian 3D points to Homogeneous 4D points.

    Args:
      pts_3d (np.ndarray, torch.Tensor): 3D points in Cartesian coord, could be Nx3 or BxNx3 (tensor only).

    Returns:
      nx4 points in Homogeneous coord.
    """
    return_tensor = isinstance(pts_3d, torch.Tensor)
    if not return_tensor:  # return np.ndarray
        if pts_3d.ndim != 2 or pts_3d.shape[1] != 3:
            raise RuntimeError(f"The size of pts should be Nx3, but got {pts_3d.shape}")
        pts_3d = pts_3d.copy()
        return np.concatenate([pts_3d, np.ones([pts_3d.shape[0], 1])], axis=1)
    else:
        if pts_3d.ndim == 2:
            if pts_3d.shape[1] != 3:
                raise RuntimeError(f"The size of pts should be Nx3 or BxNx3, but got {pts_3d.shape}")

            pts_3d = pts_3d.clone()
            return torch.cat([pts_3d, torch.ones(pts_3d.shape[0], 1).to(pts_3d.device)], dim=1)
        else:
            if pts_3d.shape[2] != 3:
                raise RuntimeError(f"The size of pts should be Nx3 or BxNx3, but got {pts_3d.shape}")

            pts_3d = pts_3d.clone()
            padding = torch.ones(pts_3d.shape[0], pts_3d.shape[1], 1).to(pts_3d.device)
            return torch.cat([pts_3d, padding], dim=2)
