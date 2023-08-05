// Copyright 2021 Zhihao Liang
#include <cstdint>
#include <iostream>
#include <pybind11/functional.h>

#include "cumcubes.hpp"


std::vector<torch::Tensor> mc::marching_cubes(
    const torch::Tensor& density_grid,
    const float thresh,
    const std::vector<float> lower,
    const std::vector<float> upper
) {
    // check
    CHECK_INPUT(density_grid);
    TORCH_CHECK(density_grid.ndimension() == 3)

    assert(lower.size() == 3);
    assert(upper.size() == 3);

    const float l[3] = {lower[0], lower[1], lower[2]};
    const float u[3] = {upper[0], upper[1], upper[2]};
    
    std::vector<Tensor> results = mc::marching_cubes_wrapper(density_grid, thresh, l, u);
    
    return results;
}


std::vector<torch::Tensor> mc::marching_cubes_func(
    const torch::Tensor& sample_points,
    const float thresh,
    const std::vector<float> lower,
    const std::vector<float> upper,
    const py::object &func
) {
    // check
    CHECK_CONTIGUOUS(sample_points);
    // CHECK_INPUT(sample_points);
    TORCH_CHECK(sample_points.ndimension() == 4);
    torch::Device curr_device = sample_points.device();
    const int32_t res_x = sample_points.size(0), res_y = sample_points.size(1), res_z = sample_points.size(2);
    const int32_t offx = res_y * res_z, offy = res_z;
    
    torch::Tensor density_grid = torch::zeros({res_x, res_y, res_z},
        torch::TensorOptions().dtype(torch::kFloat).device(curr_device));

    const float* sample_points_ptr = sample_points.data_ptr<float>();
    float* density_grid_ptr = density_grid.data_ptr<float>();

    for (int32_t i = 0; i < res_x; ++i) {
        for (int32_t j = 0; j < res_y; ++j) {
            for (int32_t k = 0; k < res_z; ++k) {
                const py::object density = func(
                    sample_points_ptr[(i * offx + j * offy + k) * 3 + 0],
                    sample_points_ptr[(i * offx + j * offy + k) * 3 + 1],
                    sample_points_ptr[(i * offx + j * offy + k) * 3 + 2]
                );
                density_grid_ptr[i * offx + j * offy + k] = density.cast<float>();
            }
        }
    }

    assert(lower.size() == 3);
    assert(upper.size() == 3);

    const float l[3] = {lower[0], lower[1], lower[2]};
    const float u[3] = {upper[0], upper[1], upper[2]};

    density_grid = density_grid.to(torch::kCUDA);
    std::vector<Tensor> results = mc::marching_cubes_wrapper(density_grid, thresh, l, u);
    
    return results;
}

void mc::save_mesh_as_ply(
    const std::string filename,
    torch::Tensor vertices,
    torch::Tensor faces,
    torch::Tensor colors
) {
    CHECK_CONTIGUOUS(vertices);
    CHECK_CONTIGUOUS(faces);
    CHECK_CONTIGUOUS(colors);
    assert(colors.dtype() == torch::kUInt8);

    if (vertices.is_cuda()) { vertices = vertices.to(torch::kCPU); }
    if (faces.is_cuda()) { faces = faces.to(torch::kCPU); }
    if (colors.is_cuda()) { colors = colors.to(torch::kCPU); }

    std::ofstream ply_file(filename, std::ios::out | std::ios::binary);
    ply_file << "ply\n";
    ply_file << "format binary_little_endian 1.0\n";
    ply_file << "element vertex " << vertices.size(0) << std::endl;
    ply_file << "property float x\n";
    ply_file << "property float y\n";
    ply_file << "property float z\n";
    ply_file << "property uchar red\n";
    ply_file << "property uchar green\n";
    ply_file << "property uchar blue\n";
    ply_file << "element face " << faces.size(0) << std::endl;
    ply_file << "property list int int vertex_index\n";

    ply_file << "end_header\n";

    const int32_t num_vertices = vertices.size(0), num_faces = faces.size(0);

    const float* vertices_ptr = vertices.data_ptr<float>();
    const uint8_t* colors_ptr = colors.data_ptr<uint8_t>();
    for (int32_t i = 0; i < num_vertices; ++i) {
        ply_file.write((char *)&(vertices_ptr[i * 3]), 3 * sizeof(float));
        ply_file.write((char *)&(colors_ptr[i * 3]), 3 * sizeof(uint8_t));
    }

    torch::Tensor faces_head = torch::ones({num_faces, 1},
        torch::TensorOptions().dtype(torch::kInt).device(torch::kCPU)) * 3;
    
    torch::Tensor padded_faces = torch::cat({faces_head, faces}, 1); // [num_faces, 4]
    CHECK_CONTIGUOUS(padded_faces);
    
    const int32_t* faces_ptr = padded_faces.data_ptr<int32_t>();
    ply_file.write((char *)&(faces_ptr[0]), num_faces * 4 * sizeof(int32_t));

    ply_file.close();
}

