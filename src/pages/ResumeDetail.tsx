import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { useMutation } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { api } from '../utils/api';

export default function ResumeDetail() {
  const navigate = useNavigate();

  const uploadMutation = useMutation(
    (file: File) => {
      const formData = new FormData();
      formData.append('file', file);
      return api.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
    },
    {
      onSuccess: (response) => {
        toast.success('Resume uploaded successfully!');
        navigate(`/resumes/${response.data.resume_id}`);
      },
      onError: () => {
        toast.error('Failed to upload resume. Please try again.');
      },
    }
  );

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      if (acceptedFiles.length > 0) {
        uploadMutation.mutate(acceptedFiles[0]);
      }
    },
    [uploadMutation]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        ['.docx'],
      'image/jpeg': ['.jpg', '.jpeg'],
    },
    maxFiles: 1,
  });

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-xl font-semibold mb-4">Upload Resume</h2>

      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors ${
          isDragActive
            ? 'border-indigo-500 bg-indigo-50'
            : 'border-gray-300 hover:border-indigo-500'
        }`}
      >
        <input {...getInputProps()} />
        <div className="space-y-2">
          <svg
            className="mx-auto h-12 w-12 text-gray-400"
            stroke="currentColor"
            fill="none"
            viewBox="0 0 48 48"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M8 14v20c0 4.418 3.582 8 8 8h16c4.418 0 8-3.582 8-8V14m-4 0l-8-8-8 8m8-8v28"
            />
          </svg>
          <div className="text-lg font-medium text-gray-900">
            {isDragActive
              ? 'Drop the resume here'
              : 'Drag and drop your resume, or click to select'}
          </div>
          <p className="text-sm text-gray-500">
            PDF, DOCX, JPG or JPEG (max. 16MB)
          </p>
        </div>
      </div>

      {uploadMutation.isLoading && (
        <div className="mt-4 text-center text-gray-600">
          Uploading and analyzing resume...
        </div>
      )}
    </div>
  );
}
