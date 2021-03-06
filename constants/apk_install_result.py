#!/usr/bin/env python
# coding=utf-8

class ApkInstallResultConstant:

    def __init__(self, sdk_version):
        self.sdk_version = sdk_version

    def get_result(self, install_result):
        if install_result == 'Success':
            return install_result
        if int(self.sdk_version) >= 23:
            return 'Failure [' + self.get_result_android_sdk_23(install_result) + ']'
        else:
            return install_result

    def get_result_android_sdk_23(self, install_result):
        if 'INSTALL_FAILED_TEST_ONLY' in install_result:
            return 'INSTALL_FAILED_TEST_ONLY'
        elif 'INSTALL_FAILED_TEST_ONLY: installPackageLI' in install_result:
            return 'INSTALL_FAILED_TEST_ONLY: installPackageLI'
        elif 'INSTALL_FAILED_VERSION_DOWNGRADE' in install_result:
            return 'INSTALL_FAILED_VERSION_DOWNGRADE'
        elif 'INSTALL_FAILED_UPDATE_INCOMPATIBLE' in install_result:
            return 'INSTALL_FAILED_UPDATE_INCOMPATIBLE'
        elif 'INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES' in install_result:
            return 'INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES'
        elif 'INSTALL_PARSE_FAILED_NO_CERTIFICATES' in install_result:
            return 'INSTALL_PARSE_FAILED_NO_CERTIFICATES'
        elif 'INSTALL_FAILED_AUTH_CERTIFICATE' in install_result:
            return 'INSTALL_FAILED_AUTH_CERTIFICATE'
        elif 'INSTALL_FAILED_INVALID_APK' in install_result:
            return 'INSTALL_FAILED_INVALID_APK'
        elif 'INSTALL_FAILED_SHARED_USER_INCOMPATIBLE' in install_result:
            return 'INSTALL_FAILED_SHARED_USER_INCOMPATIBLE'
        elif 'INSTALL_FAILED_INVALID_URI' in install_result:
            return 'INSTALL_FAILED_INVALID_URI'
        elif 'INSTALL_FAILED_INSUFFICIENT_STORAGE' in install_result:
            return 'INSTALL_FAILED_INSUFFICIENT_STORAGE'
        elif 'INSTALL_FAILED_NO_SHARED_USER' in install_result:
            return 'INSTALL_FAILED_NO_SHARED_USER'
        elif 'INSTALL_FAILED_MISSING_SHARED_LIBRARY' in install_result:
            return 'INSTALL_FAILED_MISSING_SHARED_LIBRARY'
        elif 'INSTALL_FAILED_REPLACE_COULDNT_DELETE' in install_result:
            return 'INSTALL_FAILED_REPLACE_COULDNT_DELETE'
        elif 'INSTALL_FAILED_DEXOPT' in install_result:
            return 'INSTALL_FAILED_DEXOPT'
        elif 'INSTALL_FAILED_OLDER_SDK' in install_result:
            return 'INSTALL_FAILED_OLDER_SDK'
        elif 'INSTALL_FAILED_CONFLICTING_PROVIDER' in install_result:
            return 'INSTALL_FAILED_CONFLICTING_PROVIDER'
        elif 'INSTALL_FAILED_NEWER_SDK' in install_result:
            return 'INSTALL_FAILED_NEWER_SDK'
        elif 'INSTALL_FAILED_CPU_ABI_INCOMPATIBLE' in install_result:
            return 'INSTALL_FAILED_CPU_ABI_INCOMPATIBLE'
        elif 'INSTALL_FAILED_MISSING_FEATURE' in install_result:
            return 'INSTALL_FAILED_MISSING_FEATURE'
        elif 'INSTALL_FAILED_PERMISSION_MODEL_DOWNGRADE' in install_result:
            return 'INSTALL_FAILED_PERMISSION_MODEL_DOWNGRADE'
        elif 'INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES' in install_result:
            return 'INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES'
        elif 'INSTALL_FAILED_USER_RESTRICTED' in install_result:
            return 'INSTALL_FAILED_USER_RESTRICTED'
        elif 'INSTALL_CANCELED_BY_USER' in install_result:
            return 'INSTALL_CANCELED_BY_USER'
        elif 'INSTALL_FAILED_NO_MATCHING_ABIS' in install_result:
            return 'INSTALL_FAILED_NO_MATCHING_ABIS'
        else:
            return install_result