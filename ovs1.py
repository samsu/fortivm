from neutron.agent.ovsdb import impl_vsctl
from neutron.agent.common import ovs_lib
from oslo_serialization import jsonutils

#class OvsdbVsctl(impl_vsctl.OvsdbVsctl):
#    def set_port(self, port, trunks, may_exist=True):
#        opts = ['--may-exist'] if may_exist else None
#        return BaseCommand(self.context, 'set', opts, ['port', port, "trunks=%s" % trunks])

class OVSBridge(ovs_lib.OVSBridge):
    def set_port(self, port, trunks=None, may_exist=False):
        args = ['port', port]
        if trunks:
           args.append("trunks=%s" % trunks)
        res = None
        with self.ovsdb.transaction() as txn:
            opts = ['--may-exist'] if may_exist else None
            print "args=", args
            res = txn.add(impl_vsctl.BaseCommand(self.ovsdb.context, 'set', opts, args))
        #print "res=", jsonutils.loads(res.result)
        print "res=", res.result    
        return res

    def list_port(self, port, may_exist=False, **kwargs):
        args = ['port', port]
        res = None
        with self.ovsdb.transaction() as txn:
            opts = ['--may-exist'] if may_exist else None
            print "args=", args
            print "opts=", opts
            res = txn.add(impl_vsctl.MultiLineCommand(self.ovsdb.context, 'list', opts, args))
        print "res=", res.result
        res = jsonutils.loads(res.result.pop())
        for k,v in res.iteritems():
            print "k=", k
            while isinstance(v, (list, tuple)) and 1 == len(v):
                v = v.pop() 
            print "v=", v
            res[k] = v
        a = res['headings']
        b = res['data']
        c = []
        for i in range(len(b)):
            if isinstance(b[i], (list, tuple)):
                b[i] = set(b[i][1]) if 'set' == b[i][0] else b[i][1]
        res1 = dict(zip(a, b))
        print "res1", res1
        if kwargs:
            keys = list(set(kwargs) & set(b))
            return {key: res1[key] for key in keys}
        return res1

FGT_INT_PORT='fgt-int-port'
ovs = OVSBridge('br-int')
print ovs.get_port_tag_dict()
print "T1:"
ovs.list_port(FGT_INT_PORT)
import ipdb;ipdb.set_trace()
ovs.set_port(FGT_INT_PORT, trunks='1,3,5')

#print "T2:"
#ovs.set_port(FGT_INT_PORT, trunks='1,3,5x')

