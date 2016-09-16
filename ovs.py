from neutron.agent.ovsdb import impl_vsctl
from neutron.agent.common import ovs_lib
from oslo_serialization import jsonutils

#class OvsdbVsctl(impl_vsctl.OvsdbVsctl):
#    def set_port(self, port, trunks, may_exist=True):
#        opts = ['--may-exist'] if may_exist else None
#        return BaseCommand(self.context, 'set', opts, ['port', port, "trunks=%s" % trunks])

class OVSBridge(ovs_lib.OVSBridge):
    def set_port(self, port, **kwargs):
        args = ['port', port]
        opts = None
        if kwargs:
            for k, v in kwargs.iteritems():
                args.append("%(key)s=%(val)s" % {'key': k, 'val': v})
        with self.ovsdb.transaction() as txn:
            txn.add(
                impl_vsctl.BaseCommand(self.ovsdb.context, 'set', opts, args))
        fields = tuple(key for key in kwargs)
        return self.list_port(port, *fields)

    def list_port(self, port, *fields):
        args = ['port', port]
        opts = None
        with self.ovsdb.transaction() as txn:
            res = txn.add(impl_vsctl.MultiLineCommand(self.ovsdb.context,
                                                      'list', opts, args))
        res = jsonutils.loads(res.result.pop())
        for k, v in res.iteritems():
            while isinstance(v, (list, tuple)) and 1 == len(v):
                v = v.pop()
            res[k] = v
        keys = res['headings']
        vals = res['data']
        for idx in range(len(vals)):
            if isinstance(vals[idx], (list, tuple)):
                vals[idx] = set(vals[idx][1]) if 'set' == vals[idx][0] \
                    else vals[idx][1]
        res = dict(zip(keys, vals))
        if fields:
            ret_keys = list(set(fields) & set(keys))
            return {key: res[key] for key in ret_keys}
        return res


FGT_INT_PORT='fgt-int-port'
ovs = OVSBridge('br-int')
print ovs.get_port_tag_dict()
print "T1:"
print ovs.list_port(FGT_INT_PORT, 'trunks')
a = ovs.set_port(FGT_INT_PORT, trunks='1,3')
import ipdb;ipdb.set_trace()
print a
#ovs.set_port(FGT_INT_PORT, trunks='1,3')
print ovs.list_port(FGT_INT_PORT, 'trunks')

#print "T2:"
#ovs.set_port(FGT_INT_PORT, trunks='1,3,5x')

