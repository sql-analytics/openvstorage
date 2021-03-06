// Copyright 2014 CloudFounders NV
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
/*global define */
define([
    'jquery', 'ovs/generic',
    '../build', './data', './gather_vpool', './gather_mountpoints', './gather_cinder', './confirm'
], function($, generic, build, data, GatherVPool, GatherMountPoints, GatherCinder, Confirm) {
    "use strict";
    return function(options) {
        var self = this;
        build(self);

        // Setup
        self.title(generic.tryGet(options, 'title', $.t('ovs:wizards.addvpool.title')));
        self.modal(generic.tryGet(options, 'modal', false));
        self.steps([new GatherVPool(), new GatherMountPoints(), new GatherCinder(), new Confirm()]);
        self.step(0);
        self.activateStep();

        // Cleaning data
        data.target(undefined);
        data.accesskey('');
        data.secretkey('');
        data.backend('local');
        data.mtptTemp(undefined);
        data.mtptBFS(undefined);
        data.mtptMD(undefined);
        data.mtptReadCache1(undefined);
        data.mtptReadCache2(undefined);
        data.mtptWriteCache(undefined);
        data.mtptFOC(undefined);
        data.storageIP(undefined);
        data.name('');
        data.host('');
        data.localHost(true);
        data.port(80);
        data.timeout(600);
        data.backends(['local', 'ceph_s3', 'amazon_s3', 'swift_s3', 'distributed', 'alba']);
        data.storageRouters([]);
        data.storageDrivers([]);
        data.mountpoints([]);
        data.ipAddresses([]);
        data.albaBackends(undefined);
        data.albaBackend(undefined);
        data.cinderUser('admin');
        data.cinderPassword('');
        data.cinderTenant('admin');
        data.cinderCtrlIP('127.0.0.1');
        data.configCinder(false);
        data.hasCinder(false);
    };
});
